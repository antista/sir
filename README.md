# SIR epidemic model
This is a simple program which can build a simple SIR epidemic model by given parameters
or plot current infected people plot and predict future evolution of COVID-19 disease.
* ## SIR model
SIR (susceptible-infected-recovered) model indicates the three possible states of the members of a population
afflicted by a contagious decease. [Read more](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model)
* **`beta`** is the disease transmission rate
* **`gamma`** is the rate of recovery from the disease
* **`R`** is the basic effective reproductive rate. **`R = beta/gamma`**. 
Disease is spreading if **R > 1** and if **R < 1** the disease is not spreading.

#### Usage
```
$ ./sir.sh
```
Then enter a population number and count of simulation days or set 
**POPULATION** and **DAYS_COUNT** environment variables.

On the open chart you can change **beta** and **gamma** parameters.

* ## COVID-19 simulation
Program receives open data from https://data.world/markmarkoh/coronavirus-data 
and plot the number of infected people, the average number of infected people 
and the graph of the predicted infected people.

### IMPORTANT
Before run script you should login to dataworld and get your personal access token here https://data.world/settings/advanced.
Then run `dw configure` and paste your access token there or run `export DW_AUTH_TOKEN=<YOUR_TOKEN>`.

#### Usage
```
$ ./corona.sh
```
You can set **LAST_PREDICT_DAY** variable (default is 365) as number of day from epidemic start date 
and the prediction will be built before this date.
