from flask import jsonify

class appError(Exception):
    # message -> human readable message, status code -> computer message
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        # initalize the base Exception class normally
        super().__init__(message)
    
def registerErrorHandlers(app):
    @app.errorhandler(appError)
    def handleAppError(e):
        print({"error": e.message})
        return jsonify({"error": e.message}), e.status_code
    
    @app.errorhandler(404)
    def notFound(e):
        print({"error": "Resource not found"})
        return jsonify({"error": "Resource not found (404)"}), 404
    
    @app.errorhandler(500)
    def serverError(e):
        print({"error": "Internal server error"})
        return jsonify({"error": "Internal server error (500)"}), 500
        