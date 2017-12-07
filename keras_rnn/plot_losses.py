# file to plot training and validation loss after training model. 
import pickle
import matplotlib.pyplot as plt

def main():
	with open("loss.pickle","rb") as l:
		lossdata = pickle.load(l)
		plt.plot(lossdata, label = "training loss")
	with open("val_loss.pickle","rb") as vl:
		vallossdata = pickle.load(vl)
		plt.plot(vallossdata, label = "validation loss")
	plt.legend()
	plt.show()


if __name__ == "__main__":
	main()