import requests
import json 
import sys
import gtk
import appindicator

PING_FREQUENCY = 30


def __fetch_prices():
	try:
		r = requests.get("https://coinjar-data.herokuapp.com/fair_rate.json")
		data = json.loads(r.text)
		ask = data["ask"]["AUD"]
		bid = data["bid"]["AUD"]
		spot = data["spot"]["AUD"]
	except:
		ask = "NA"
		bid = "NA"
		spot = "NA"
	return ask, bid, spot

class CheckPrices:
	def __init__(self):
		self.ind = appindicator.Indicator("debian-doc-menu","btc",appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appindicator.STATUS_ACTIVE)
		self.ind.set_attention_icon("btc")

		self.menu_setup()
		self.ind.set_menu(self.menu)

		self.last_spot = 0

	def menu_setup(self):
		self.menu = gtk.Menu()

		self.quit_item = gtk.MenuItem("Quit")
		self.quit_item.connect("activate", self.quit)
		# Set the ask as a menu item 
		self.ask = gtk.MenuItem("Ask \tLoading")
		self.ask.show()
		self.menu.append(self.ask)
		# Set the spot as a menu item 
		self.spot = gtk.MenuItem("Spot \tLoading")
		self.spot.show()
		self.menu.append(self.spot)
		# Set the bid as a menu item 
		self.bid = gtk.MenuItem("Bid \tLoading")
		self.bid.show()
		self.menu.append(self.bid)
	def fetch_prices(self):
		ask, bid, spot = self.retrieve()
		self.ask.set_label("Ask \t$ %s"%ask)
		self.bid.set_label("Bid \t$ %s"%bid)
		self.spot.set_label("Spot \t$ %s"%spot)
			
		# Change the color of the icon based on the move	
		if spot > self.last_spot:
			self.ind.set_icon("btc-green")
		elif spot == self.last_spot:
			self.ind.set_icon("btc")
		else:
			self.ind.set_icon("btc-red")
	
	def retrieve(self):
		try:
			r = requests.get("https://coinjar-data.herokuapp.com/fair_rate.json")
			data = json.loads(r.text)
			ask = data["ask"]["AUD"]
			bid = data["bid"]["AUD"]
			spot = data["spot"]["AUD"]
		except:
			ask = "NA"
			bid = "NA"
			spot = "NA"
		return ask, bid, spot

	def main(self):
		self.fetch_prices()
		gtk.timeout_add(PING_FREQUENCY * 1000, self.fetch_prices)
		print "bid"
		gtk.main()
	def quit(self, widget):
		sys.exit(0)


if __name__ == '__main__':
	#ask, bid, spot = __fetch_prices()
	indicator = CheckPrices()
	indicator.main()