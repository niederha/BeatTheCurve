
# coding: utf-8
import numpy as np
from   scipy.integrate import odeint
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import geonamescache
import csv
import requests
import json
import pycountry


###### Global Variables ######

# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 2.4/11, 1./11 #multiplied by 36 
#mortality rate
m = 3./100

#Quarantine: isolation of symptomatic people
Quarantine = {"no":0, "yes":0.75} #yes: percentage of sick people showing symptoms

#Hygiene level
Hygiene = {"dirty":0.5, "normal":1.0, "medium":1.5, "high":2.0} 

#Supermarket frequency
shopping_freq = {"very low":1, "low": 2,"normal":3,"high":5,"very high":6,"everyday":7} #number of days you go shopping/week

#Social distancing
pop_dist = {"100%":1, "90%":0.9, "75%":0.75, "50%":0.5, "25%":0.25, "0%":0} # % of the population practicing social distancing
level_dist = {"isolation":0, "very high": 1, "high":2, "moderate":4, "low":6, "none":8} #how many ppl you see in 1 day if you are distancing


# Computation:

#SIRD classical model
def deriv_basic(y, t, N, beta, gamma, day, beds):
    #differential equations without mesures
    
    S, I, R, De = y
   
    #risk people
    Severe    = I* 0.20 #require hos
    
    #check hospital capacity
    if Severe > beds: 
        m_r = 2*m
    else: m_r = m
    
    
    #diff eq
    dSdt = -beta * S*I/ N
    dIdt = beta * S*I / N - gamma * I
    dRdt = (1-m_r)*gamma * I
    dDedt = gamma*m_r*I
    
    return dSdt, dIdt, dRdt, dDedt

    
# The SIRD model differential equations with mesures
def deriv(y, t, N, beta, gamma, day, StartQ, Q, current_hygiene, StartH, current_shop, 
        dist, StartD, dayBTN, beds): 
    S, I, R, De = y
    
    #quarantined people
    impact_Q = Quarantine[Q]
    q=0
    if day >= StartQ:
        q = I*impact_Q
        
       
    #risk people
    Severe    = I* 0.2 #require hosp

    
    #check hospital capacity
    if Severe > beds: 
        m_r = 2*m
    else: m_r = m
      
    #adapt beta to hygiene
    h_impact = Hygiene[current_hygiene]
    if day >= StartH:
        beta = beta/h_impact
        
    #adapt beta to supermarket frequency
    shop_impact = shopping_freq[current_shop]
    beta = beta/2**(np.log(shopping_freq["normal"]/shop_impact)/np.log(5))
    #everytime shopping freqency is divided by 5, beta/2
   
    #social distancing
    dist_impact = [pop_dist[dist[0]], level_dist[dist[1]]]
    beta2 = 0
    I1 = I
    I2 = 0
    if day >= StartD:
        beta2 = beta*dist_impact[1]**2/64. #beta of ppl distancing
        
        I1 = I*(1-dist_impact[0]) #proportion of infected not distancing
        I2 = I*dist_impact[0] #proportion of ppl distancing
        
    #diff eq
    dSdt = -(beta * S * I1 + beta2 * S * I2 - beta * S * q) / N
    dIdt = (beta * S * I1 + beta2 * S * I2 - beta * S * q)/ N - gamma * I
    dRdt = (1-m_r)*gamma * I
    dDedt = gamma*m_r*I
    

    return dSdt, dIdt, dRdt, dDedt

def sir_no_mesures(sim_length, deriv_basic, y0, t, N, beta, gamma, beds):
    
    S0, I0, R0, D0 = y0
    S_array = np.ones(sim_length)*S0
    I_array = np.ones(sim_length)*I0
    R_array = np.ones(sim_length)*R0
    De_array = np.zeros(sim_length)
    Severe   = np.zeros(sim_length)

    for i in range(1, sim_length):
        ret = odeint(deriv_basic, y0, t, args=(N, beta, gamma, i, beds ))
        S, I, R, De = ret.T
        
        S_array[i]   = S[1]
        I_array[i]   = I[1]
        R_array[i]   = R[1]
        De_array[i]  = De[1]
        Severe[i]    = I[1]* 0.2 #require hosp
        y0 = S[1], I[1], R[1], De[1]
        
    #information for the table
    #data = [[N], [I0], [beta/gamma], [m], ["never"], [float("inf")], [beds], [resp], ["normal"]]
    
    return S_array, I_array, R_array, De_array, Severe
                     
                 
def sir(sim_length, deriv, deriv_basic, y0, t, N, beta, gamma, StartQ, Q, current_hygiene, StartH, current_shop, 
        dist, startD, DayBTN, beds):
    
    S0, I0, R0, D0 = y0
    #initialize array
    S_array = np.ones(sim_length)*S0
    I_array = np.ones(sim_length)*I0
    R_array = np.ones(sim_length)*R0
    De_array = np.zeros(sim_length)
    Severe   = np.zeros(sim_length)
    
    # Integrate the SIRD equations over the time grid, t.
    for i in range(1,sim_length):
        if i >= DayBTN:
            ret = odeint(deriv_basic, y0, t, args=(N, beta, gamma, i))
        else:
            ret = odeint(deriv, y0, t, args=(N, beta, gamma, i, StartQ, Q, current_hygiene, StartH, current_shop, 
                        dist, startD, DayBTN, beds))
    
    
        S, I, R, De = ret.T
        S_array[i]   = S[1]
        I_array[i]   = I[1]
        R_array[i]   = R[1]
        De_array[i]  = De[1]
    
        Severe[i]    = I[1]* 0.2 #require hosp
        y0 = S[1], I[1], R[1], De[1]
        
     #information for tables
    quarantine_start = "Never"
    if Q != 0:
        quarantine_start = StartQ

    #data = [[N], [I0], [beta/gamma], [m], [quarantine_start], [DayBTN], [beds], [resp], [current_hygiene]]
    
    return S_array, I_array, R_array, De_array, Severe

def get_beds(Country_ISO):
    N = get_population(Country_ISO)
    file = 'sir_simul/hosp_beds.csv'
    with open(file) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            beds = row[Country_ISO]
    beds = float(beds) * 0.5  # half of the beds available for epidemics
    beds = beds / 1000 * N  # total nb of beds in country
    return beds

def get_population(Country_ISO):
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    country = countries.get(Country_ISO)

    # prevent from crashng if ISO code wrong
    if country == None:
        N = 8 * 10 ** 7
    else:
        N = country.get('population')

    return N

def getIRD(Country_ISO):
    I0 = 0
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"
    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "815636d2f5msh5b6f6b41061625ep10f46fjsn4221a8a8f565"
    }
    response = requests.request("GET", url, headers=headers)
    a = json.loads(response.text)
    stat = (a['countries_stat'])

    country = pycountry.countries.get(alpha_2=Country_ISO)
    # protect from crashing in case ISO code not found
    if country == None:
        country_name = "not found"
    else:
        country_name = country.name

    # corrected names manually
    if country_name == "United Kingdom":
        country_name = "UK"
    elif country_name == "United States":
        country_name = "USA"

    for i in stat:
        if i['country_name'] == country_name:
            I0 = i['cases']
            R0 = i['total_recovered']
            D0 = i['deaths']

            # convert to float
            I0 = float(I0.replace(",", ""))
            R0 = float(R0.replace(",", ""))
            D0 = float(D0.replace(",", ""))
            break

    # fallback in case country_names don't match
    if I0 == 0:
        I0 = 70000
        R0 = 0
        D0 = 0

    return I0, R0, D0


###### Users parameters function#####

def simulateUsersbehaviour(friends, central_loc, hands, sim_length, deriv, deriv_basic, y0, t, N, beds):
    #simulates what would happen if everyone had the same behaviour as the user
    #the number of people he has seen outside his household (friends),the number of times he's been to a highly frequented 
    #location in the past week (central_loc) and the number of times he washed his hand in the last day (hands)
    #returns the deaths, infections, immunes, suceptibles, severe and critical cases, number of ppl saved

    
    #finding level of social distancing
    if friends == 0:
        level = "isolation"
    elif 0 < friends <=1.5:
        level = "very high"
    elif 1.5 < friends <= 2.5:
        level = "high"
    elif 2.5 < friends <= 5:
        level = "moderate"
    elif 5 < friends <= 7:
        level = "low"
    else:
        level = "none"  
    dist = ["90%",level]
    
    #finding level of hygiene
    if hands < 3:
        curr_hygiene = "dirty"
    elif 3 <= hands < 5:
        curr_hygiene = "normal"
    elif 5 <= hands < 10:
        curr_hygiene = "medium"
    else:
        curr_hygiene = "high"
    
    #finding frequency of central location
    if central_loc <=1:
        curr_shop = "very low"
    elif 1 < central_loc <= 2.5:
        curr_shop = "low"
    elif 2.5 < central_loc <= 4:
        curr_shop = "normal"
    elif 4 < central_loc <= 5.5:
        curr_shop = "high"
    elif 5.5 < central_loc < 6.5:
        curr_shop = "very high"
    else:
        curr_shop = "everyday"
    
    return sir(sim_length, deriv, deriv_basic, y0, t, N, beta, gamma, float("inf"), "no", curr_hygiene, 0, 
               curr_shop, dist,0, float('inf'), beds)



####COMPUTE SAVINGS#####
def compute_saving(friends=10, central_loc=3, hands=3, Country_ISO="CH", sim_length=300):
    t= [0,1]
    # compute how many people saved from death and infection

    S, I, Recovered, De, Severe, beds, Country_ISO = main(friends, central_loc, hands, Country_ISO)

    R = Recovered + De
    # get country population
    N = get_population(Country_ISO)

    I0, R0, D0 = getIRD(Country_ISO)
    S0 = N-I0-R0
    y0 = S0, I0, R0, D0

    S_nm, I_nm, R_nm, De_nm, Severe = sir_no_mesures(sim_length, deriv_basic, y0, t, N, beta, gamma, beds)
    S, I, Recovered, De, Severe, beds, Country_ISO = main(friends, central_loc, hands, Country_ISO)
    R = Recovered+De
    # infections:
    Tot_i = R[len(R) - 1]
    Tot_i_nm = R_nm[len(R_nm) - 1]
    Saved_i = Tot_i_nm - Tot_i
    Saved_i = Saved_i / N

    # deaths
    Tot_d = De[len(De) - 1]
    Tot_d_nm = De_nm[len(De_nm) - 1]
    Saved_d = Tot_d_nm - Tot_d
    Saved_d = Saved_d / N
    return Saved_i, Saved_d

###MAIN#####

#Input: 
#friends: number of friends in contact with during a day
#central_loc: nb of days per week you go to supermarket
#hands: nb of time per day you wash your hands
#Country_ISO
#simulation length (OPTIONAL)

 
def main(friends=10, central_loc=3, hands=3, Country_ISO="CH", sim_length=300):
    t=[0,1]

    #get country population
    N = get_population(Country_ISO)
    
    #get country infected, dead, recovered (real time):
    I0, R0, D0 = getIRD(Country_ISO)

    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0
    y0 = S0, I0, R0, D0

    #get nb beds
    beds = get_beds(Country_ISO)

    S, I, R, De, Severe = simulateUsersbehaviour(friends, central_loc, hands, sim_length, deriv, deriv_basic, y0, t, N, beds)
    Recovered = R-De
    
    return S, I, Recovered, De, Severe, beds, Country_ISO

#S, I, Recovered, De, Severe, beds, Country_ISO =  main(friends, central_loc, hands, Country_ISO)













