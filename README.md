# Yoder Covid Tracker

https://ancient-dawn-31373.herokuapp.com/

Covid data tracker for counties with family members

## Data Sources

*  New York Times Covid Data
	*  [NYT Github](https://github.com/nytimes/covid-19-data)
	*  Daily records for cases and deaths by county. Data is brought into the tracker dail.
* Pennsylvania data
	* 	**26/07/2021 UDPATE** - PA data is no longer pulled from PA DOH; it now comes from the same NTY data that the other counties do. Due to the unbelievable length of time this thing has gone on combined with database row limits on free Heroku databases, I can no longer fit the PA data in separate tables :(
	* 	[Penn's Department of Health](https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx)
	*  Data for the counties in Pennsylvania are pulled directly from the DOH website.
*  Covid ActNow
	*  [Covid ActNow](href=https://covidactnow.org/)
	*  This is where the r value and testing positivity data are pulled from. Data is pulled from their api daily.
	*  **13/09/2021 UDPATE**  - Some counties \*cough King County cough* are having trouble getting their positivity rates calculated. I'm pretty sure this is the counties fault and not CovidActNow. When it happens, the county's page reports that the rate hasn't been calculated recently.  
*  **21/09/2021 Update**- DuPage County, IL is no longer included in the tracker. I ran into the limit on database size that comes with the free Heroku dyno (again). If this thing doesn't end soon (not holding out hope tbh), The database will need a new schema to fit all of the data from all counties and all time.

*  **21/12/2021 Update**- DuPage County, IL is back in folks. I did indeed run into the row limit on the free heroku postgres db again. instead of dropping more counties, I combined the NYT table with the CovidActNow metrics table. It is a little more janky, but it cut the number of rows in half almost, so unless we have another two years of this sh*t, that should no longer be an issue.