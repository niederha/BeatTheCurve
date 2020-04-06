import sir_simul.sir_simul as s
S, I, Recovered, De, Severe, beds, Country_ISO = s.main(10,3,3,"DE")

print(beds, Country_ISO)
