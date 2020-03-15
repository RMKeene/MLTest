
3/12/2020 - Richard Keene

LOG of work thought and process:

3/12/2020
The code has little error checking.  I believe the purpose of this programming test is to 
look at ideas on matching students to courses, so that is the focus.
More maintainable code would be better for actual production code, with unit tests and much more.

Also much of the focus here is that the main.py be easily runnable. So lots of conditional setup is done
on-the-fly if not already done.

- Python 3.8
- PyCharm
- Made Git Project https://github.com/RMKeene/MLTest
- Initial checkin of empty project
- Copied in default .gitignore from python.org
- Made venv
- Unpacked Pluralsight files
- Setup Flask, copied in standard REST example code.  Modified to naming for my project
- Got all working with Postman
- Got SQLite3 downloaded.
- Made the database init code.

3/13/2020 - COVID-19 gets serious in America. Friday the Thirteenth?
- Got all 4 tables into SQLite3 from CSVs.  
- Got auto-load code working to setup and load to db if not already loaded.
- One can just delete keene.db to force a data reload.
- Now to think about actual algorithms......

3/14/2020 - Thoughts
- The requirement is to find similarity however one wants
- Similar interests
- Similar abilities (scores on assessments)
- Similar training courses ( spending habits $ )
- Similar interest vs. courses choices.  Do they choose what they are interested in, or are they choosing to expand their horizons.
- Similar ability vs. courses choices.  Do they choose to stretch learning, or refresh existing abilities.
- Number of courses.  Are they the 20% that represent 80% of revenue? (Assumes all courses equal cost)
- Are the continual learners vs. a burst of learning over a short time period?
- Course speed. Do they trickle through a course or binge the course?
- Are they fast at courses, for a given course they are the race horse, or the turtle?
- Ability breadth. Are their test scores on a wide range of topics, or a narrow focus?
- CS vs. Art vs. Animation vs. game vs. web vs. other skill categories.

3/15/2020 - Implementation
- Decided to do K-Mean clustering on courses vs interests.
- Got REST working better.  More readable JSON output so easier on future developers.

