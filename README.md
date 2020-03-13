
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