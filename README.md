My API Project

Welcome to the My API Project! This project provides a RESTful API for managing patients and images. It includes functionality for adding, updating, retrieving, and deleting data related to patients and images. The API is built using Flask, with a focus on simplicity and scalability.
Table of Contents

   . Features
   . Technologies Used
   . Installation
   . Running the API
   . API Documentation
   . Usage
       . Create a Patient
       . Retrieve a Patient
       . Upload an Image
       . Delete an Image
   . Testing
   . Contributing
   . License

Features

   . Patient Management: Create, retrieve, update, and delete patient records.
   . Image Management: Upload, retrieve, and delete images associated with patients.
   . Data Validation: Ensure correct data input formats for patients and images.
   . Health Check: Basic health check endpoint to ensure API availability.
   . Swagger Integration: API documentation via Swagger UI for easy testing and understanding.

Technologies Used

   . Python 3.9
   . Flask - A lightweight WSGI web application framework.
   . SQLAlchemy - ORM for database interactions.
   . PyTest - For writing and running tests.
   . Docker - Containerization for the application.


Installation

   1. Clone the repository:
      git clone https://github.com/farshad-bit/mein-api-projekt.git
      cd my-api-project

  2. Set up a virtual environment:
      python3 -m venv venv
      source venv/bin/activate  # For Windows: venv\Scripts\activate

  3. Install the dependencies:
      pip install -r requirements.txt

  4. Set up the database:

    You will need to set up your database (MySQL, PostgreSQL, etc.) and configure the connection in the .env file.

  5. Environment variables:

    Create a .env file in the root directory with the following information:

    FLASK_ENV=development
      DATABASE_URL=mysql://username:password@localhost/db_name
      SECRET_KEY=your_secret_key


    Running the API
    Using Flask CLI

    To run the API locally, use the following command:
    flask run

    The API will be available at http://127.0.0.1:5000/.
  Using Docker

  Alternatively, you can use Docker to run the API in a container.

   1. Build the Docker image:
        docker build -t my-api-project .

   2. Run the container:
      docker-compose up


  The API will be available at http://localhost:5000/.
  API Documentation

  The API documentation is available through Swagger UI. Once the API is running, you can access the Swagger documentation at:
  http://localhost:5000/swagger/
  This will provide interactive documentation where you can test the API endpoints.

  Usage
  Create a Patient
    POST /patients
  Request body:
    {
    "first_name": "John",
    "last_name": "Doe",
    "dob": "1980-01-01",
    "gender": "male",
    "physician": "Dr. Smith",
    "ancestry": "Caucasian",
    "eyeid": "12345"
      }

   Retrieve a Patient
     GET /patients/{patient_id}

  Upload an Image
    POST /patients/{patient_id}/images
    Request body (multipart/form-data):

  image_path: The image file to upload.
    

  Delete an Image
    DELETE /images/{image_id}

  Testing

  Unit tests are written using PyTest.

  To run the tests, use the following command:
    pytest
    You can also run the tests inside the Docker container by running:
    docker-compose exec web pytest

  Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes or improvements.
Steps to Contribute:

   1. Fork the repository.
   2. Create a new branch (git checkout -b feature/my-feature).
   3. Commit your changes (git commit -m 'Add some feature').
   4. Push to the branch (git push origin feature/my-feature).
   5. Open a Pull Request.

License

This project is licensed under the MIT License. See the LICENSE file for details







      

                  
