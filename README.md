# syllabus-scrap-into-graph

### About

Aim of the project was to create graph database of AGH Univerity's Syllabus subset and create a graph database from it. An app was supposed to be a way to easily access database by simple search input.

AGH's Syllabus:

![syllabus](https://user-images.githubusercontent.com/62848991/217253651-76d21417-0243-430e-b1a3-4900a18d40b2.png)

The project involved extracting from the sylabuss website data on every possible subject in our department (such as semester, lecturer, hours, description, etc.), creating from this data a graph database mapping all the relationships contained in this data, and building an application or interface that allows users to browse and search the data contained in the database.

### Build with

Syllabus scrappnig was preformed using BeautifulSoup library [2] , graph database was created in Neo4j [3] and as for the simple web application Flask framework [4] was used.

### Design

In our project, we wanted to present the most important information taken from the Syllabus. However, it was also important for us that the data in the database were useful and possible for further processing. Database was focused on basic information about the subject, its scope (whether it has a lecture, project and laboratory classes) as well as lecturers and coordinators. Below is a "diagram" designed by us for a single item.

![database_scheme](https://user-images.githubusercontent.com/62848991/217253682-cf5f374d-025f-4caa-ae59-60d64b00c3fd.jpg)

Simple web app consisted of one search input, that was used for searching any match of that phrase in database. It look like this:

![s1](https://user-images.githubusercontent.com/62848991/217256900-606f9385-2d3b-4621-877a-85784d27a440.png)

### References

[1] Syllabus AGH (https://sylabusy.agh.edu.pl/pl/1/2/18/1/4/16)

[2] BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/)

[3] Neo4j (https://neo4j.com/)

[4] Flask (https://flask.palletsprojects.com/en/2.2.x/)
