import sys
import fileinput

# Fixed_T: Always predict taken
# Static_F: Start false, flip on miss
# Bimodal: Follows 2bit algorithm
# Coded with Python 3

# Cache table class which adds the address and status of the branch
class BHT_CACHE:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, address):
        if address not in self.cache:
            return -1
        self.order.remove(address)
        self.order.append(address)
        return self.cache[address]

    def put(self, address, set):
        if address in self.cache:
            self.order.remove(address)
        elif len(self.cache) == self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[address] = set
        self.order.append(address)
        pass


# Only predicts taken
def fixedt(data):
    c_pred = 0
    for i in range(len(data)):
        if data[i][1] == "@":
            c_pred += 1
    print("Fixed_T: ", c_pred, " / ", len(data))


# StaticF Functions as a tflipflop, if the prediction is wrong it will flip the next prediction for the branch.
def staticf(data):
    c_pred = 0
    prediction = None
    status = ['N', 'T']
    cache = BHT_CACHE(512)
    for i in range(len(data)):
        address = bin(int(data[i][0], 16))[2:].zfill(48)
        branch_val = data[i][1]
        if cache.get(address) == -1:
            cache.put(address, status[0])
            set_status = status[0]
        else:
            set_status = cache.get(address)
            cache.put(address, set_status)
        if set_status == status[0]:
            prediction = '.'
        else:
            prediction = '@'
        if prediction is branch_val:
            c_pred += 1
        else:
            if set_status == status[0]:
                cache.put(address, status[1])
            elif set_status == status[1]:
                cache.put(address, status[0])
            else:
                print("Error: set_status not found")
    print("Static_F: ", c_pred, " / ", len(data))


# Bi modal will make a prediction based on the last 2 prediction outcomes with the following values:
# 00 (Strongly NT), 01 (Weakly NT), 10 (Weakly T), 11 (Strongly T)
def bimodal(data):
    c_pred = 0
    prediction = None
    status = ['00', '01', '10', '11']
    cache = BHT_CACHE(512)
    for i in range(len(data)):
        address = bin(int(data[i][0], 16))[2:].zfill(48)
        branch_val = data[i][1]
        if cache.get(address) == -1:
            cache.put(address, status[1])
            set_status = status[1]
        else:
            set_status = cache.get(address)
            cache.put(address, set_status)
        if set_status == status[0] or set_status == status[1]:
            prediction = '.'
        else:
            prediction = '@'
        if prediction is branch_val:
            c_pred += 1
            if set_status == status[0]:
                continue
            elif set_status == status[1]:
                cache.put(address, status[0])
            elif set_status == status[2]:
                cache.put(address, status[3])
            elif set_status == status[3]:
                continue
        else:
            if set_status == status[0]:
                cache.put(address, status[1])
            elif set_status == status[1]:
                cache.put(address, status[3])
            elif set_status == status[2]:
                cache.put(address, status[0])
            elif set_status == status[3]:
                cache.put(address, status[2])
    print("Bimodal: ", c_pred, " / ", len(data))

    c_pred = 0
    prediction = None
    status = ['00', '01', '10', '11']
    cache = BHT_CACHE(512)
    for i in range(len(data)):
        address = bin(int(data[i][0], 16))[2:].zfill(48)
        branch_val = data[i][1]
        if cache.get(address) == -1:
            cache.put(address, status[1])
            set_status = status[1]
        else:
            set_status = cache.get(address)
            cache.put(address, set_status)
        if set_status == status[0] or set_status == status[1]:
            prediction = '.'
        else:
            prediction = '@'
        if prediction is branch_val:
            c_pred += 1
            if set_status == status[0]:
                continue
            elif set_status == status[1]:
                cache.put(address, status[0])
            elif set_status == status[2]:
                cache.put(address, status[3])
            elif set_status == status[3]:
                continue
        else:
            if set_status == status[0]:
                cache.put(address, status[1])
            elif set_status == status[1]:
                cache.put(address, status[3])
            elif set_status == status[2]:
                cache.put(address, status[0])
            elif set_status == status[3]:
                cache.put(address, status[2])
    print("2_Layer: ", c_pred, " / ", len(data))


# Main function takes in the trace file, formats it into tracedata, and runs the algorithms
def main():
    trace = sys.argv[1]
    tracedata = []

    for line in fileinput.input(files=trace):
        tracedata.append(line.strip("\n").split("\t"))

    fixedt(tracedata)  
    staticf(tracedata) 
    bimodal(tracedata)  


if __name__ == "__main__":
    main()
