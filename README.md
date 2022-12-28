# SheepFish test task


#### Before running project

- Create local env file
- Build containers
- Run project

#### Create local env 

```
python3 -m venv venv
source venv/bin/activate (Linux and macOS) or 
venv\Scripts\activate (Windows)
```


#### Build containers and run

```docker-compose up --build```


#### When project is running

- Apply db migrations `python manage.py migrate`
- Run local server `python manage.py runserver`

### Project description
The service receives information about a new order, creates checks in the database for all printers of the point specified in the order.
An asynchronous worker using wkhtmltopdf to generate a PDF file from an HTML template.

