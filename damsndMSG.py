import smtplib
from email.message import EmailMessage

def bestValues(filename):
    f = open(filename)
    ff = f.readlines()
    err = []
    cost = []
    ncoefs = []
    for line in ff:
        err.append(float(line.split()[0]))
        cost.append(float(line.split()[1]))
        ncoefs.append(float(line.split()[2]))
        minerr = min(err)
        mincost = min(cost)
        coeferr = ncoefs[err.index(minerr)]
        coefcost = ncoefs[cost.index(mincost)]
    return minerr, mincost, coeferr, coefcost



EMAIL_ADRESS = 'yipiyupilandia@gmail.com'
EMAIL_PASSWORD = 'rauzaruk'
filename1 = "results/errcostval.txt"
filename2 = "results/gauss.txt"
filename3 = "results/gaussworld.txt"


msg = EmailMessage()
msg['Subject'] = "Resultados del Entrenamiento SPEECON"
msg['From'] = EMAIL_ADRESS
msg['To'] = EMAIL_ADRESS

error,cost,coeferr,coefcost = bestValues(filename1)
error,cost,gausserr,gausscost = bestValues(filename2)
error,cost,worlderr,worldcost = bestValues(filename3)

content = f'Hola,\n\nLos valores óptimos son:\n- Número de Coeficientes: {coefcost}\n- Número de Gausianas: {gausscost}\n- Número de Gaussianas World: {worldcost}\n- Error cometido: {error}\n- Coste: {cost}\n\nSaludos'
msg.set_content(content)
print(content)
with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
    smtp.send_message(msg)