import argparse
import inspect
import json
import re
import sys


class MaintainNFIHolds: 
    def __init__(self):
        self._nfi_hold_file = 'user_data/nfi-hold-trades.json'
        pass

    def _load_data(self):
        with open(self._nfi_hold_file) as f: #specify the file name
            return json.load(f)


    def _load_nfi_hold(self) :
        """The load_hold_trades() method loads hold_trades data from a JSON file.
        :return: json object
        """
        return self._load_data()


    def _save_nfi_hold(self,json_data):
        """The save_data() json method saves data to a JSON file.

        :return: None
        """
        with open(self._nfi_hold_file, 'w') as f:
            json.dump(json_data, f, indent=4)


    def add_trade_pair(self, pair, profit):
        """The save_hold_trade() method lists hold_trades data from a JSON file.
        "trade_pairs":
        {
            "LUNA/USDT": 0.001, 
            "ETH/USDT": -0.02
        }
        :param pair: Pair to buy (ETH/BTC)
        :param profit: Optional - percent i.e. 0.005 or -0.005
        :return: json object
        """

        _hold_trades = self._load_nfi_hold()
        _hold_trades["trade_pairs"][pair] = float(profit)
        #for i in trade_pairs["trade_pairs"]:
        #    _hold_trades["trade_pairs"][i] = trade_pairs["trade_pairs"][i]
        self._save_nfi_hold(_hold_trades)
        self.list_trade_pair()

    def remove_trade_pair(self, pair):
        """The remove_trade_pair() method removes a trade_pair from JSON file.
        :param pair: Pair to remove (ETH/BTC)
        :return: json object
        """

        self.list_trade_pair()
        _hold_trades = self._load_nfi_hold()
        try:
            del _hold_trades["trade_pairs"][pair]
        except KeyError:
            print("Key " + pair + " not exists.")

        self._save_nfi_hold(_hold_trades)
        self.list_trade_pair()


    def list_trade_pair(self) :
        """The list_trade_pair() method lists trade_pairs from a JSON file.
        "trade_pairs":
        {
            "LUNA/USDT": 0.001, 
            "ETH/USDT": -0.02
        }
        :return: json object
        """
        json_data = self._load_data()
        
        print(str(json.dumps(json_data["trade_pairs"], indent=4)))
        
    def add_trade_id(self, pair, profit):
        """The add_trade_id() method adds a trade_id to a JSON file.
        "trade_pairs":
        {
            "3": 0.001, 
            "13": -0.02
        }
        :param pair: Pair to buy (ETH/BTC)
        :param profit: Optional - percent i.e. 0.005 or -0.005
        :return: json object
        """

        _hold_trades = self._load_nfi_hold()
        _hold_trades["trade_ids"][pair] = float(profit)
        #for i in trade_pairs["trade_pairs"]:
        #    _hold_trades["trade_pairs"][i] = trade_pairs["trade_pairs"][i]

        self._save_nfi_hold(_hold_trades)
        self.list_trade_ids()

    def remove_trade_id(self, pair):
        """The remove_trade_id() method removes a trade_id from JSON file.
        :param pair: Pair to remove (ETH/BTC)
        :return: json object
        """

        self.list_trade_ids()
        _hold_trades = self._load_nfi_hold()
        try:
            del _hold_trades["trade_ids"][pair]
        except KeyError:
            print("Key " + pair + " not exists.")

        self._save_nfi_hold(_hold_trades)
        self.list_trade_pair()


    def list_trade_ids(self) :
        """The list_hold_trades() method lists trade_ids from a JSON file.
        "trade_pairs":
        {
            "LUNA/USDT": 0.001, 
            "ETH/USDT": -0.02
        }
        :return: json object
        """
        json_data = self._load_data()
        
        print(str(json.dumps(json_data["trade_ids"], indent=4)))
        
    def help(self):
        """The list_hold_trades() method lists trade_ids from a JSON file.
        "trade_pairs":
        {
            "LUNA/USDT": 0.001, 
            "ETH/USDT": -0.02
        }
        :return: json object
        """
        print("Possible commands:\n")
        for x, y in inspect.getmembers(self):
            #print ("A" + str(x))
            #print("B" + str(y))
            if not x.startswith('_'):
                doc = re.sub(':return:.*', '', getattr(maintain_nfi_holds, x).__doc__, flags=re.MULTILINE).rstrip()
                docstring = "".join([i + "\n" for i in doc.splitlines() if i.strip().startswith(":param")])
                print(f"{x}\n\t{docstring}\n")

    

def print_commands():
    # Print dynamic help for the different commands using the commands doc-strings
    maintain_nfi_holds = MaintainNFIHolds()
    print("Possible commands:\n")
    for x, y in inspect.getmembers(maintain_nfi_holds):
        #print ("A" + str(x))
        #print("B" + str(y))
        if not x.startswith('_'):
            doc = re.sub(':return:.*', '', getattr(maintain_nfi_holds, x).__doc__, flags=re.MULTILINE).rstrip()
            print(f"{x}\n\t{doc}\n")

def main(args):
    if args.get("show"):
        print_commands()
        sys.exit()

    maintain_nfi_holds = MaintainNFIHolds()

    m = [x for x, y in inspect.getmembers(maintain_nfi_holds) if not x.startswith('_')]
    command = args["command"]
    if command not in m:
        print(f"Command {command} not defined")
        print_commands()
        return

    getattr(maintain_nfi_holds, command)(*args["command_arguments"])


def add_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("command",
                        help="Positional argument defining the command to execute.",
                        nargs="?"
                        )


    parser.add_argument('--show',
                        help='Show possible methods with this api',
                        dest='show',
                        action='store_true',
                        default=False
                        )


    parser.add_argument("command_arguments",
                        help="Positional arguments for the parameters for [command]",
                        nargs="*",
                        default=[]
                        )



    args = parser.parse_args()
    return vars(args)

if __name__ == "__main__":
    args = add_arguments()
    main(args)
