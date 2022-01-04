import hashlib, hmac
import math
import binascii

import time

import collections
import json

CLIENT_SEED = b'0000000000000000004d6ec16dafe9d8370958664c1dc422f452892264c59526'




# DICT = {336: 1, 245: 1, 319: 1, 300: 1, 372: 1, 331: 1, 317: 1, 265: 1, 349: 1, 303: 1, 311: 1, 357: 1, 308: 1, 503: 1, 296: 1, 302: 1, 237: 1, 293: 1, 391: 1, 291: 1, 326: 1, 405: 1, 572: 1, 329: 1, 446: 1, 272: 1, 360: 1, 361: 1, 387: 1, 287: 1, 324: 1, 312: 1, 258: 1, 322: 1, 295: 1, 353: 1, 313: 1, 460: 1, 321: 1, 363: 1, 404: 1, 323: 1, 252: 1, 408: 1, 342: 1, 344: 1, 320: 1, 315: 1, 286: 1, 233: 1, 290: 1, 333: 1, 335: 1, 359: 1, 297: 1, 299: 1, 348: 1, 280: 1, 373: 1, 263: 1, 254: 2, 277: 2, 301: 2, 284: 2, 250: 2, 249: 2, 271: 2, 269: 2, 395: 2, 285: 2, 228: 2, 223: 2, 243: 2, 248: 2, 307: 2, 261: 2, 267: 2, 240: 2, 362: 2, 246: 2, 343: 2, 244: 2, 289: 2, 253: 2, 325: 2, 257: 3, 235: 3, 220: 3, 275: 3, 266: 3, 276: 3, 251: 3, 288: 3, 279: 3, 219: 3, 213: 3, 256: 3, 231: 3, 212: 3, 238: 3, 259: 3, 230: 3, 283: 4, 270: 4, 239: 4, 232: 4, 242: 4, 264: 4, 260: 4, 225: 4, 210: 5, 208: 5, 222: 5, 209: 5, 234: 5, 255: 5, 229: 5, 203: 5, 236: 6, 199: 6, 205: 6, 224: 6, 211: 6, 198: 6, 197: 6, 207: 6, 226: 6, 204: 7, 227: 7, 179: 7, 214: 7, 206: 7, 201: 7, 193: 7, 176: 7, 196: 7, 218: 7, 200: 8, 215: 8, 184: 8, 191: 9, 221: 9, 183: 9, 194: 10, 187: 10, 192: 10, 180: 10, 185: 11, 163: 11, 172: 11, 161: 11, 186: 11, 177: 12, 181: 12, 170: 12, 157: 12, 174: 13, 202: 13, 195: 13, 159: 13, 190: 13, 164: 13, 188: 13, 178: 13, 171: 13, 166: 14, 169: 14, 182: 14, 160: 14, 216: 14, 154: 15, 175: 15, 173: 15, 165: 16, 168: 16, 189: 16, 148: 17, 167: 17, 158: 17, 156: 17, 152: 18, 142: 19, 162: 19, 147: 19, 146: 20, 145: 20, 150: 20, 138: 21, 139: 22, 149: 22, 130: 22, 144: 22, 153: 22, 137: 23, 151: 23, 143: 23, 140: 24, 128: 24, 141: 26, 127: 26, 129: 28, 136: 29, 155: 31, 131: 32, 134: 32, 121: 33, 126: 34, 135: 34, 133: 35, 110: 35, 132: 36, 124: 37, 109: 38, 119: 38, 125: 38, 114: 39, 116: 40, 113: 40, 115: 41, 103: 41, 123: 41, 122: 43, 106: 44, 112: 44, 111: 45, 108: 45, 117: 46, 118: 47, 102: 47, 120: 47, 93: 49, 95: 50, 107: 50, 105: 51, 99: 51, 98: 53, 96: 56, 104: 57, 97: 58, 92: 60, 101: 61, 94: 63, 90: 63, 88: 64, 89: 65, 81: 69, 86: 69, 78: 70, 91: 70, 100: 70, 85: 73, 79: 74, 84: 74, 87: 80, 82: 80, 75: 81, 80: 82, 83: 82, 74: 85, 77: 86, 69: 91, 70: 92, 72: 93, 65: 93, 67: 93, 73: 95, 76: 99, 62: 100, 68: 110, 71: 111, 66: 114, 60: 116, 64: 117, 56: 120, 57: 120, 63: 122, 61: 122, 59: 133, 50: 134, 58: 139, 46: 139, 49: 140, 55: 143, 51: 144, 53: 147, 54: 150, 47: 154, 52: 155, 40: 156, 48: 158, 43: 160, 33: 168, 44: 169, 39: 174, 45: 176, 41: 176, 42: 177, 38: 182, 37: 182, 32: 198, 36: 200, 34: 211, 25: 213, 35: 217, 26: 226, 31: 233, 29: 234, 28: 236, 30: 237, 24: 240, 27: 245, 23: 258, 21: 265, 22: 265, 18: 266, 19: 267, 17: 273, 15: 282, 16: 284, 20: 284, 14: 312, 13: 317, 7: 318, 11: 322, 12: 324, 8: 332, 10: 338, 5: 364, 9: 364, 6: 368, 1: 377, 2: 381, 4: 389, 3: 396}







def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# THIS WORKS
# print(encrypt_string('2709df525f4eb261cdf97b94e872929727e7ce94e1ba6bfb6c7a830f7d48fc64'))


def gameResult(seed):
    nBits = 52 # number of most significant bits to use
    nBitsToUse = 13 # nBits/4

    # // 1. HMAC_SHA256(key=salt, message=seed)
    # hmac = crypto.createHmac("sha256", salt)
    # hmac.update(seed)
    # seed = hmac.digest("hex")

    raw = binascii.unhexlify(seed)

    # seed = hmac.new(CLIENT_SEED, seed.encode(), 'sha256').hexdigest()

    seed = hmac.new(CLIENT_SEED, raw, digestmod=hashlib.sha256).hexdigest()

    # print("seed", seed)

    # // 2. r = 52 most significant bits
    # seed = seed.slice(0, nBits/4)
    seed = seed[0:nBitsToUse]
    r = int(seed, 16)

    # // 3. X = r / 2^52
    X = r / math.pow(2, nBits) # uniformly distributed in [0; 1)

    # // 4. X = 99 / (1-X)
    X = 99 / (1 - X)

    # 5. return max(trunc(X), 100)
    result = math.floor(X);
    return max(1, result / 100);





STARTING_SEED = 'bc739a50573ced7b252fde71e35a7c78191dee0d500abff0afa20e4510df39f9'

def generate_historical_data(fileName="history", skip=0):
    n = 10000000
    i = 0
    # skip = 0#10000000

    l = collections.deque()
    h = STARTING_SEED

    while i < n:
        bust = gameResult(h)
        if (skip == 0):
            l.appendleft(bust)
            i += 1
        else:
            skip -= 1
        h = encrypt_string(h)
        

    x = [num for num in l]

    f = open(fileName, 'w')
    json.dump(x, f)
    f.close()
    print("DONE")



generate_historical_data("10mil1", 0)
generate_historical_data("10mil2", 10000000)
generate_historical_data("10mil3", 20000000)
generate_historical_data("10mil4", 40000000)
generate_historical_data("10mil5", 50000000)

exit(1)






# print(gameResult('6aec0eb22d930c7e0314160ee3656c1efba1313e0e841edc3dd3651790ba016f'))

# start_time = time.time()
# n = 3000000

# index = 0
# og_h = '6d2d78b52e7f4eb216ea81fab18b04fa1854a340c963d6596314c54596924abc'

# h = og_h

# got_one_index = 0
# got_one_total_index = 0

# got_one_indexes = {}
# # got_one_total_indexes_average_ones = []

# avg_percent = 0#got_one_total_index / index



# while index < n:
#     bust = gameResult(h)
#     # print(index, bust, int(avg_percent*100))

#     if (bust == 1):
#         got_one_indexes[got_one_index] = got_one_indexes.get(got_one_index, 0) + 1
#         got_one_index = 0
#         got_one_total_index += 1
#         avg_percent = got_one_total_index / index

#     index += 1
#     got_one_index += 1

#     h = encrypt_string(h)

#     # if (got_one_total_index > 4):
#     #     print(got_one_indexes)
#     #     break


# print(avg_percent, got_one_total_index, index)

# SORTED_DICT = {k: v for k, v in sorted(got_one_indexes.items(), key=lambda item: item[1])}

# # print(SORTED_DICT)

# print("took", time.time() - start_time)




