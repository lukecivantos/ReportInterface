# ReportInterface
This Flask App runs using Heroku and can be found live at https://hpt-revenue-reports.herokuapp.com/admin. 

Ticket Sales Managers for the Hasty Pudding Theatricals have to go through each sale through Authorize.net and 
create an excel for the Finance Manager who then does reconciliations. This Flask App allows users to upload txt files
and download the finished Revenue Reports. The app cannot categorize a purchase when patrons donate on top of a ticket purchase,
so it just labels them as "Donation on top of ticket." The Ticket Sales Managers then just have to review for these cases so the dollar
amount and ticket type (Boston, New York, Bermuda; Weekday, weekend) are specified. 
