import json

def store_listing(file, symbol):
    """
    Save listing into local json file
    """
    
    with open(file, "w") as f:
        json.dump(symbol, f, indent=4)
        
def load_listing(file):
    """
    Update Json file
    """
    with open(file, "r+") as f:
        return json.load(f)