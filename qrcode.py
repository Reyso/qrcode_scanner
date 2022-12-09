# bibliotecas necessarias

from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="output_data.csv",
	help="path to output CSV file containing QR data")
args = vars(ap.parse_args())

# Inicializa o vídeo
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0) #delay

# abre o aquivo csv onde será salvo os logs


csv = open(args["output"], "w")
found = set()


# loop sobre os frames do vídeo 

while True:
	
	# define o tamanho  do vídeo mostrado
	frame = vs.read()
	frame = imutils.resize(frame, width=600)

	# objeto decoficador para qrcode
	barcodes = pyzbar.decode(frame)

    	# loop atraves da figura até encontrar o conteúdo do qrcode
	for barcode in barcodes:
		# Cria os BOUNDING BOX ao redor da figura
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

		# Precisamos converter o objeto qrcode para string
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		# Imprime o conteúdo do qrcode na tela
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) # cor

		# escreve em um arquivo CSV a saída do qrcode
		if barcodeData not in found:
			csv.write("{},{}\n".format(datetime.datetime.now(),
				barcodeData))
			csv.flush()
			found.add(barcodeData)

	# Mostra a saída do frame
	cv2.imshow("QR code Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# Precinar q para fechar a aplicação
	if key == ord("q"):
		break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
#csv.close()
cv2.destroyAllWindows()
vs.stop()
