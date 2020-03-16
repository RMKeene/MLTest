
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
- Decided to do a score on courses vs interests. 
- Got REST working better.  More readable JSON output so easier on future developers.
- Hmmmmmmm, "calculate a score that represents similarity between users". This could be anything
   from trivial grouping to complex AI with learned weighting between groups.  Just a matter of 
   how much time to put into this exercise.  Going to KISS it. (Keep it Simple Stupid™)
- Courses vs Interests.  Lets make this a ranking of how many course key words match interest key words. Where 0 is a
  user that has no commonality of interests to courses, and 1.0 is heavy match.  This may reveal
  some grouping or maybe a spectrum of users that are 'normal' vs. 'strange' Or maybe 
  people that are changing career? Or forced to take training by their employer?
- Could do a fancy SQL Join and do the whole thing in on SQL statement, but I want control over the 
  way interest and course tags are compared.  So will instead do it explicitly.  And, hey, CPU cycles are
  free here at home.
- Got correlation going.  Very very slow code.  Lots of loops on database queries.  Would be way faster to preload
  all the table data into ram and crunch it. But if zillions of users maybe not, so then partition the problem 
  or pre-crunch the data into correlated sets.
  
Results:
- Ok, got results.  Users have a score on how much commonality there is between their 
  stated interests and the courses they take. Many are 0.0.  Some are in the 0.5 range.
  Math is common interest count / (total interest count + 1) 
-
