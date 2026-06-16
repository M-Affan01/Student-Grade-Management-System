"""
Flask Application Entry Point (MVC - App)
==========================================
Creates and configures the Flask application with CORS, storage backend,
error handlers, and route registration. This is the main entry point
for the Student Grade Management System backend.

MVC Architecture:
    - Model: models/student.py, models/student_list.py
    - View: views/response.py (response formatting)
    - Controller: controllers/student_controller.py (route handlers)
    - App: This file (wiring everything together)


create_app(): Factory function that creates and configures the Flask app.
"""


from flask import Flask, jsonify
from flask_cors import CORS
from database.storage_factory import create_storage
from controllers.student_controller import student_bp
from views.response import storage_info_view, error_response
import traceback
import os


def create_app():
    """Create and configure the Flask application.

    Initializes CORS, storage backend, blueprint registration,
    and error handlers. The storage type defaults to MySQL with
    JSON fallback.

    Storage is stored as app.storage for access by controllers
    via current_app.storage.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app)

    # Determine storage type from environment variable (default: mysql)
    storage_type = os.environ.get("STORAGE_TYPE", "mysql")
    storage = create_storage(storage_type)

    # Attach storage to app for access in controllers via current_app
    app.storage = storage
    app.storage_type = storage_type

    # Register the student controller blueprint
    app.register_blueprint(student_bp)

    # ─── Error Handlers ──────────────────────────────────────────────────

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify(error_response("Resource not found", str(error), 404)), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return jsonify(error_response("Method not allowed", f"{error}", 405)), 405

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server Error."""
        return jsonify(error_response("Internal server error", status=500)), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all uncaught exceptions with traceback logging."""
        traceback.print_exc()
        return jsonify(error_response("Server error", str(e), 500)), 500

    # ─── Storage Management Routes ───────────────────────────────────────

    @app.route("/api/storage/info", methods=["GET"])
    def storage_info():
        """Get information about the active storage backend.

        Returns:
            JSON with storage type, student count, and backend-specific details.
        """
        try:
            return jsonify(storage_info_view(app.storage_type, app.storage))
        except Exception as e:
            return jsonify(error_response(str(e), status=500)), 500

    @app.route("/api/storage/save", methods=["POST"])
    def save_data():
        """Manually save data to the storage backend.

        For JSON: writes to file. For MySQL: no-op (auto-saved).

        Returns:
            JSON with success or error message.
        """
        try:
            if hasattr(app.storage, "save"):
                result = app.storage.save()
                if result:
                    return jsonify({"message": "Data saved successfully"})
                return jsonify(error_response("Failed to save data", status=500)), 500
            return jsonify({"message": "Auto-saved (MySQL)"})
        except Exception as e:
            return jsonify(error_response("Failed to save", str(e), 500)), 500

    @app.route("/api/storage/load", methods=["POST"])
    def load_data():
        """Manually reload data from the storage backend.

        For JSON: re-reads the file. For MySQL: re-queries the database.

        Returns:
            JSON with success message and student count.
        """
        try:
            if hasattr(app.storage, "load"):
                app.storage.load()
                return jsonify({"message": "Data loaded successfully", "count": app.storage.size()})
            return jsonify({"message": "Auto-loaded (MySQL)"})
        except Exception as e:
            return jsonify(error_response("Failed to load", str(e), 500)), 500

    @app.route("/api/health", methods=["GET"])
    def health():
        """Health check endpoint for monitoring.

        Returns:
            JSON with 'status', 'storage' type, and 'students_count'.
        """
        return jsonify({"status": "ok", "storage": app.storage_type, "students_count": app.storage.size()})

    return app


# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Run the Flask development server on port 5002
    app.run(debug=False, host="0.0.0.0", port=5002)
