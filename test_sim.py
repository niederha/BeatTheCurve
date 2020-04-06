import numpy as np
import matplotlib.pyplot as plt
import sir_simul.sir_simul as s


def plot_sir(S, I, R, time):
    # plot SIR
    fig1 = plt.figure(facecolor='w')
    plt.plot(time, S / 1000, 'b', alpha=0.5, lw=2, label='Susceptible')
    plt.plot(time, I / 1000, 'r', alpha=0.5, lw=2, label='Infected')
    plt.plot(time, R / 1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    plt.xlabel('Time /days')
    plt.ylabel('Number (1000s)')

    # colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    # plt.table(cellText=data, rowLabels=rows, rowColours=colors, loc='top')
    # legend = plt.legend()
    plt.show()
    # plt.savefig('NoMesSIR.png', bbox_inches="tight", pad_inches=1)


# plots severe, critical case and deaths
def plot_letality(Severe, Death, time, beds):
    fig2 = plt.figure(facecolor='w')
    plt.plot(time, Severe / 1000, 'm', alpha=0.5, lw=2, label='severe cases')
    plt.plot(time, Death / 1000, 'r', alpha=0.5, lw=2, label='Death')

    plt.plot([0, len(time)], [beds / 1000, beds / 1000], 'k', label='beds')

    # colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    # plt.table(cellText=data, rowLabels=rows, rowColours=colors, loc='top')

    plt.xlabel('Time /days')
    plt.ylabel('Number (1000s)')
    legend = plt.legend()
    # plt.savefig('NoMesD.png', bbox_inches="tight", pad_inches=1)


# pie chart Infected/Dead
def pie_id(De, R, N):
    Tot_death = De[len(De) - 1]
    Percentage_death = Tot_death / N * 100
    Tot_infected = R[len(R) - 1]
    Percentage_infected = Tot_infected / N * 100

    # Pie Chart
    labels = 'Dead', 'Infected', 'Not infected'
    sizes = [Percentage_death, Percentage_infected, 100 - Percentage_death - Percentage_infected]
    # explode = (0.1, 0.1, 0)

    fig3, ax3 = plt.subplots()
    ax3.pie(sizes, explode=None, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.savefig('NoMesPie.png')

    plt.show()

S, I, Recovered, De, Severe, beds, Country_ISO = s.main(0,"moderate", "normal", "yes", 3)


#Saved_I, Saved_D = s.compute_saving(3, 3, 3, "DE")
N = S[0]+I[0]+Recovered[0]+De[0]
plot_sir(S, I, Recovered+De, np.linspace(0, 300, 300))
pie_id(De, Recovered+De, N)
plot_letality(Severe, De, np.linspace(0, 300, 300), beds)
