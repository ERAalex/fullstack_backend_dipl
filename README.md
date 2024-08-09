
#### E.R.A. - Espinosa Rozov Alexander - python developer.
# Cloud Store project - keep your files safe.

<img src="https://github.com/ERAalex/fullstack_backend_dipl/blob/main/project_image.jpg">
<p>
  <a href="https://www.linkedin.com/in/alexander-espinosa-rozov-b3b270121/"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"></a>
</p>
<br>
<p><a href="https://github.com/ERAalex" target="_blank">➡️ Check out my acc.</a></p>

## Attention 
In this github repository is only part of a store cloud project, 
Checkout frontend part: 

<p><a href="https://github.com/ERAalex/fullstack_frontend_dipl" target="_blank">➡️ Go to frontend.</a></p>

You can contact me:
<br><a href="mailto:erapyth@gmail.com"><img src="https://img.shields.io/badge/-Gmail%20contact%20me-red"></a>
<br><a href="https://t.me/espinosa_python"><img src="https://img.shields.io/badge/-Telegram-blue"></a>

## About the project.

  <a href="#" target="_blank" rel="noreferrer nofollow">
      <img src="https://github.com/ERAalex/PREVIEW_project_site_buisness_card_Maria-/blob/main/website_icons.jpg" >
    </a>

This is a web application that functions as a cloud storage system. The application will allow users to view, upload, send, download, and rename files.:  <br>
- The cloud storage interface displays files uploaded by the user with key information: file name, comment, size, upload date, and last download date. <br>
- For each file, the following operations are available: delete, rename, view (in the browser or by downloading to a local disk), copy a special link to the file for granting access to other users or using it as a resource in web applications.
- All pages of the application contain a navigation menu that changes based on the user’s authentication status: “Login”, “Logout”, and “Register” buttons.
etc.

Additionally, there is an Administrative Section. The administrative interface includes the following functions:
- User registration — with validation of input data to meet the requirements described above.
- Retrieve the list of users.
- Delete a user.
- User authentication.
- User logout.

## Technologies
Main:<br/>
[![SkillIcons](https://skillicons.dev/icons?i=python)](https://skillicons.dev) PYTHON - Django <br/>
[![SkillIcons](https://skillicons.dev/icons?i=react)](https://skillicons.dev) JS - React <br/>

DATABASES:<br/>
[![SkillIcons](https://skillicons.dev/icons?i=postgres)](https://skillicons.dev) PostgreSQL <br/>

Additional tech:<br/>
[![SkillIcons](https://skillicons.dev/icons?i=git)](https://skillicons.dev) GIT <br/>
[![SkillIcons](https://skillicons.dev/icons?i=docker)](https://skillicons.dev) DOCKER <br/>
[![SkillIcons](https://skillicons.dev/icons?i=linux)](https://skillicons.dev) Linux <br/><br/>

[![SkillIcons](https://skillicons.dev/icons?i=html)](https://skillicons.dev) HTML <br/>
[![SkillIcons](https://skillicons.dev/icons?i=css)](https://skillicons.dev) CSS <br/>
<br/><br/>

## To start backend part of project:
To facilitate the project setup, a working Dockerfile, Docker Compose file, and scripts for proper project initialization have been prepared.
- Download the project. 
- Configure the .env file (an example is provided in .env-example). 
- run docker-compose up -d

THE project was tested by MacOS environment


## Creating the First Administrator

To set up the first administrator for the application, follow these steps:

1. **Set the Administrator Password:**
   - Ensure the password for the administrator is specified in the `.env` file.

2. **Use the Endpoint:**
   - **Endpoint:** `POST http://localhost:8000/api/create-admin/`

3. **Required Parameters:**
   - `username`: The username for the new administrator.
   - `email`: The email address for the new administrator.
   - `password`: The password for the new administrator (must be set in the `.env` file).
   - `code`: A verification code required for creating the administrator.

4. **Example Request:**

    ```bash
    curl -X POST http://localhost:8000/api/create-admin/ \
    -H "Content-Type: application/json" \
    -d '{
        "username": "admin",
        "email": "admin@example.com",
        "password": "your_password_here",
        "code": "verification_code"
    }'
    ```

    Alternatively, you can use Postman or a similar tool to send the request.

This request will create the first administrator for the application.

<br/>
<h2>GitHub Stats</h2>

<a href="#">![Github stats](https://github-readme-stats.vercel.app/api?username=ERAalex&theme=blueberry&count_private=true&hide_border=true&line_height=20)</a>
<a href="#">![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=ERAalex&layout=compact&theme=blueberry&count_private=true&hide_border=true)</a>
