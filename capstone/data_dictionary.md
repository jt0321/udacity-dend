
from the NTTO dataset

- i94yr: year of travel
- i94mon: month of travel
- i94res: code for country of origin
- res: long-form country of origin
- i94port: code for port of entry
- port: long-form port of entry
- i94bir: age in years
- i94addr: intended destination, as in state
- age_mean: mean age of each aggregated group
- count: number of members in each aggregated group

from the airports dataset

- ident: airport code, generally the ICAO code; can be considered the primary key for this table
- name: name of airport
- type: type of airport; possible values are small_airport, medium_airport and large_airport
- iso_country: country
- iso_region: country and state/province
- municipality: city or metropolitan area in which airport situated

from the cities dataset (self-explanatory)

- City: can be considered the primary key for this table
- State Code
- Median Age
- Total Population
- Foreign-born
- Foreign-born %: 100 * (Foreign Born / Total Population)