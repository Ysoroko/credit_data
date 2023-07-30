import csv
from locale import atof
from matplotlib import pyplot as plt # not in standard lib
from datetime import datetime, date

DATA_FILE = 'new_data_file.csv' # name of the 'csv' file 
START_DATE = datetime(2023,1,1)
MONTHLY_FEES = 1169.90
CREDIT_DURATION = 300

# Returns the number of months passed since the start of the credit
def n_months_passed():
	today = date.today()
	return ((today.year - START_DATE.year) * 12 + today.month - START_DATE.month) + 1

def clean_kbc_data():
	with open(DATA_FILE) as data_file:
		line_reader = csv.reader(data_file)
		i = 0

		with open("new_data_file.csv", 'w', newline="") as new_file:
			writer = csv.writer(new_file)
			for row in line_reader:
				if i < 239 and i:
					line = row[0].split(' ')
					# print(line)
					# print(line[2])
					amortissement_capital = atof(line[1].replace(",","."))
					paiement_interet = atof(line[2].replace(",","."))
					solde_restant_du = atof(line[5].replace(",",".") + line[6].replace(",","."))
				elif i >= 239 and i < 300:
					line = row[0].split(' ')
					amortissement_capital = atof(line[1].replace(",",".") + line[2].replace(",",".")) 
					paiement_interet = atof(line[3].replace(",","."))
					solde_restant_du = atof(line[6].replace(",",".") + line[7].replace(",","."))
				elif i == 300:
					amortissement_capital = 1165.43
					paiement_interet = 2.95
					solde_restant_du = 0
				if i:
					writer.writerow([i, amortissement_capital, paiement_interet, 1169.90, solde_restant_du])
					# print(f"[{i}]: AMORTISSEMENT [{amortissement_capital}]	| INTERET [{paiement_interet}]	| SOLDE RESTANT DU [{solde_restant_du}]")
				i+=1


double_colors_stack = [
	["#FF9B9B", "#CBFFA9"], # Lime and raspberry
	["#F4D160", "#75C2F6"], # Yellow and Blue
	["#c6743d", "#f1ddcf"], # Brown and beige
]
def draw_double_graph(axes, n_figure, values, title):
	start_angle = 45
	explode_for_two = [0.1, 0]
	autopct = '%.2f %%'
	pctdistance = 0.6
	offset = 100

	rounded_values = [round(values[0], 2), round(values[1], 2)]
	labels = [f"Payé \n\n   {rounded_values[0]} €", f"A payer \n\n   {rounded_values[1]} €"]
	colors = double_colors_stack.pop()
	

	a = axes[n_figure].pie(values, labels = labels, startangle = start_angle, explode=explode_for_two, colors=colors, autopct=autopct, pctdistance=pctdistance)
	axes[n_figure].set_title(title)


if __name__ == "__main__":
	months_passed = n_months_passed()
	already_paid = MONTHLY_FEES * months_passed
	left_to_pay = 0

	amortissement_paid = 0
	amortissement_left_to_pay = 0

	interest_paid = 0
	interest_left_to_pay = 0
	

	
	#1	548.03 €	621.87 €	1,169.90 €	245,151.97 €
	with open(DATA_FILE) as data_file:
		line_reader = csv.reader(data_file)
		i = 1
		for row in line_reader:
			if i <= months_passed:
				amortissement_paid += atof(row[1])
				interest_paid += atof(row[2])
			else:
				amortissement_left_to_pay += atof(row[1])
				interest_left_to_pay += atof(row[2])
			i+=1
		left_to_pay = interest_left_to_pay + amortissement_left_to_pay
	# print(f"LEFT TO PAY: [{left_to_pay}]")
	# print(f"AMORTISSEMENT PAID: [{amortissement_paid}]")
	# print(f"AMORTISSEMENT LEFT TO PAY: [{amortissement_left_to_pay}]")
	# print(f"INTEREST PAID: [{interest_paid}]")
	# print(f"INTEREST LEFT TO PAY: [{interest_left_to_pay}]")
	# print(f"TIME PASSED: {months_passed}")
	# print(f"TOTAL PAID: {months_passed * MONTHLY_FEES}")

	fig, axes = plt.subplots(1, 3, layout="constrained", figsize=(200, 200))
	


	# Amortissements
	draw_double_graph(axes, 0, [amortissement_paid, amortissement_left_to_pay], "Crédit")

	# Interets
	draw_double_graph(axes, 1, [interest_paid, interest_left_to_pay], "Intêrets")

	# Total
	draw_double_graph(axes, 2, [float(already_paid), float(left_to_pay)], "Total")

	fig.suptitle('Crédit Logement')
	plt.show()