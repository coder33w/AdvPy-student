import hashlib
import random
import socket
import threading

class Challenge :
    def __init__ (self, \
                  name=None, \
                  description=None, \
                  example_input=None, \
                  example_output=None, \
                  inputs=None, \
                  success_hash=None, \
                  special_solve_function=None) :
        self.name = name
        self.description = description
        self.example_input = example_input
        self.example_output = example_output
        self.inputs = inputs
        self.success_hash = success_hash
        self.special_solve_function = special_solve_function

    def validate (self, f, debug=False) :
        r = False

        if self.special_solve_function :
            r = self.special_solve_function(self.inputs, f)
        else :
            result = []
            for i in self.inputs :
                tmp = f(*i)
                if debug :
                    print i, tmp
                result.append(tmp)
            r = ''.join(map(lambda x: str(x), result))
        
        h = hashlib.sha1(r).hexdigest()
        if not self.success_hash :
            return h
        elif h == self.success_hash :
            return "FLAG: " + hashlib.sha1("FLAG" + r).hexdigest()
        else :
            return "FAIL"


class PseudoRandom :
    def __init__ (self, seed) :
        self.seed = seed

    '''
        Why do we do this? This allows us to have multiple instantiations of
        PseudoRandom and use them in a single-threaded application to produce
        predictable outputs. Threading multiple PseudoRandoms is not recommended
        as it will create a race condition.
    '''
    def advance_seed (self) :
        random.seed(self.seed)
        self.seed = random.randint(0, 1024 * 1024)

    def float (self) :
        self.advance_seed()
        return random.random()

    def number (self) :
        self.advance_seed()
        return random.randint(0, 1024 * 1024)

    def string (self, length=64) :
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.'
        self.advance_seed()
        r = []
        for i in range(length) :
            r.append(characters[random.randint(0, len(characters) - 1)])
        return ''.join(r)

def random_number_list (list_size, list_num, seed, num_max=1024*1024) :
    pseudoRandom = PseudoRandom(seed)
    return map(lambda y: map(lambda x: pseudoRandom.number() % num_max, range(list_size)), range(list_num))

def random_string_list (list_size, list_num, seed) :
    pseudoRandom = PseudoRandom(seed)
    return map(lambda y: map(lambda x: pseudoRandom.string(), range(list_size)), range(list_num))



def dict_0_make (seed, num=8) :
    pseudoRandom = PseudoRandom(seed)
    d = {}
    for i in range(num) :
        d[pseudoRandom.string(20)] = pseudoRandom.number()
    return d


def dict_1_make (seed, min_num=3, max_num=8, dict_chance=0.33) :
    pseudoRandom = PseudoRandom(seed)
    d = {}
    key_function = pseudoRandom.number
    if pseudoRandom.number() % 2 == 0 :
        key_function = pseudoRandom.string
    for i in range((pseudoRandom.number() % (max_num - min_num)) + min_num) :
        value_float = pseudoRandom.float()
        if value_float < dict_chance :
            d[key_function()] = dict_1_make(pseudoRandom.number(), dict_chance=dict_chance/1.5)
        elif (value_float - dict_chance) * (1 / dict_chance * 2) < 0.5 :
            d[key_function()] = pseudoRandom.number()
        else :
            d[key_function()] = pseudoRandom.string()
    return d

class SimpleBindTcp (threading.Thread) :
    def __init__ (self, port, inputs) :
        threading.Thread.__init__(self)
        self.port = port
        self.inputs = inputs
        self.listen_lock = threading.Lock()
        self.listen_lock.acquire()

    def run (self) :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("localhost", self.port))
        sock.listen(1)
        self.listen_lock.release()
        for i in self.inputs :
            clientsock = sock.accept()[0]
            clientsock.sendall('%d,%d' % (i[0], i[1]))
            clientsock.close()
        sock.close()

def socket_0_solve (inputs, f) :
    t = SimpleBindTcp(9999, inputs)
    t.start()
    t.listen_lock.acquire()
    t.listen_lock.release()

    r = []
    for i in range(len(inputs)) :
        r.append(f())

    return ''.join(map(lambda x: str(x), r))

class Solve1 (threading.Thread) :
    def __init__ (self, port, inputs) :
        threading.Thread.__init__(self)
        self.port = port
        self.inputs = inputs
        self.listen_lock = threading.Lock()
        self.listen_lock.acquire()

    def run (self) :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("localhost", self.port))
        sock.listen(1)
        self.listen_lock.release()

        clientsock = sock.accept()[0]
        sock.close()
        for i in self.inputs :
            clientsock.sendall(",".join(map(lambda x: str(x), i)) + "\n")

            data = ""
            while len(data) < 1024 :
                tmp = clientsock.recv(1)
                if not tmp :
                    clientsock.close()
                    return
                if tmp == '\n' :
                    break
                data += tmp
            
            thesum = int(data)
            if thesum != reduce(lambda x, y: x + y, i) :
                clientsock.sendall("bye\n")
                clientsock.close()
        
        clientsock.sendall("\n")
        clientsock.close()

def socket_1_solve (inputs, f) :
    t = Solve1(9998, inputs)
    t.start()
    t.listen_lock.acquire()
    t.listen_lock.release()
    result = f()
    return str(result)

challenge_data = [
  {
    "name": "example-0",
    "description": "Create a function which receives a string and returns that string",
    "example_input": "HELLO_WORLD",
    "example_output": "HELLO_WORLD",
    "inputs": random_string_list(1, 256, 0),
    "success_hash": "41fe4384e3b29e820cf63b3476662e4db9c638db"
  },
  {
    "name": "example-1",
    "description": "Create a function which receives two numbers and returns the result of these two numbers added together.",
    "example_input": "1024, 4021",
    "example_output": "4045",
    "inputs": random_number_list(2, 256, 1),
    "success_hash": "b00a9a4e2028a5e206eb79c82abc8422913ccb09"
  },
  {
    "name": "arith-0",
    "description": "Create a function which receives a number and returns True if the number is odd, and False if the number is even.",
    "example_input": "10101",
    "example_output": "False",
    "inputs": random_number_list(1, 256, 2),
    "success_hash": "3d8da3f66faad8c74a7556ac769a283d198684c2"
  },
  {
    "name": "arith-1",
    "description": "Create a function which receives a number and returns True if the number is divisible by 7, and False otherwise.",
    "example_input": "10101",
    "example_output": "True",
    "inputs": random_number_list(1, 256, 3),
    "success_hash": "79100e67bd460c2d466734c621852c818d022aa2"
  },
  {
    "name": "arith-2",
    "description": "Create a function which receives a number and returns the number of prime factors.",
    "example_input": "10101",
    "example_output": "4",
    "inputs": random_number_list(1, 256, 4),
    "success_hash": "aa5c2701cc48814a0750d47732dd320260190fd9"
  },
  {
    "name": "arith-3",
    "description": "Create a function which receives a number, iterates over the number, and continually concatenates FIZZ-, BUZZ-, or FIZZBUZZ- to a string. Each time the iterator is divisible by 3 you should concatenate FIZZ-, each time the iterator is divisible by 5 you should concatenate BUZZ-, and each time the number is divisible by both 3 and 5 you should concatenate FIZZBUZZ-. Leave the trailing -.",
    "example_input": "30",
    "example_output": "FIZZ-BUZZ-FIZZ-FIZZ-BUZZ-FIZZ-FIZZBUZZ-FIZZ-BUZZ-FIZZ-FIZZ-BUZZ-FIZZ-FIZZBUZZ-",
    "inputs": random_number_list(1, 256, 5, num_max=1000),
    "success_hash": "96ed21318897111bbbb8f2f1989f6e004ef0aaeb"
  },
  {
    "name": "list-0",
    "description": "Create a function which receives a list of numbers, and returns a new list only including the elements with an odd value.",
    "example_input": "[1, 2, 5, 6, 9, 10, 11, 13, 14]",
    "example_output": "[1, 5, 9, 11, 13]",
    "inputs": map(lambda x: [x], random_number_list(16, 256, 6)),
    "success_hash": "908f98e61b51921abb00cef92ff30cf5dfc15b40"
  },
  {
    "name": "list-1",
    "description": "Create a function which receives two lists of numbers, and returns a list where each element in the returned list is the sum of the elements in the passed lists.",
    "example_input": "[1, 2, 3, 4], [2, 4, 6, 8]",
    "example_output": "[3, 6, 9, 12]",
    "inputs": map(lambda x: random_number_list(x[0] % 32 + 1, 2, x[1]), random_number_list(2, 256, 7)),
    "success_hash": "9d82e3ae038808ffd6cba4b2751f68ac3a2f7caa"
  },
  {
    "name": "list-2",
    "description": "Create a function which receives a list of numbers, and returns a list with all odd numbers sorted in ascending order followed by all even numbers sorted in descending order.",
    "example_input": "[1, 2, 3, 4, 8, 7, 6, 5]",
    "example_output": "[1, 3, 5, 7, 8, 6, 4, 2]",
    "inputs": map(lambda x: [x], random_number_list(32, 256, 8)),
    "success_hash": "6ed02c952a62e12da2c01f99628616e3d177328d"
  },
  {
    "name": "dict-0",
    "description": "Create a function which receives a dictionary with keys of type string and values of type number, sorts all keys by the 4th through 16th substring indices inclusive, and returns a list of the values retrieved by their sorted keys.",
    "example_input": "{'3jltPDOUCdpz6Fd4vFgn': 794773, 'Yfig8q0X9LZB0Vg0u98Y': 699455, 'mtPMdKcD4qxreUsD9HEJ': 986350, '9dOig7fii8osvxEegRWD': 312620, 'BLdewdg2j4BaokHt776w': 1000816, 'JTG1rE1Hr1K8m6YlY1bY': 761289, 'naPoUBteiODlfYaul5JA': 183885, 'oKSvTAdqGZboaJhNgd2E': 427954}",
    "example_output": "[699455, 794773, 427954, 183885, 986350, 312620, 761289, 1000816]",
    "inputs": map(lambda x: [dict_0_make(x[0], num=(x[1] % 32 + 1))], random_number_list(2, 128, 9)),
    "success_hash": "4a030130a20e58439ff73c638e09ea6624b42f03"
  },
  {
    "name": "dict-1",
    "description": "Create a function which receives a dict. The values of this dict are strings, numbers, or more dicts of strings, numbers and dicts. They keys of each dict will be either all numbers or all strings. You must convert all dicts into lists, with all values ordered by their sorted keys. Dicts may be empty.",
    "example_input": "{206226: {624229: {'CueiYnVERqMECiCSQovh2J5.KDOeYFU.dWDI3Hx6.AorMSmSuA_6rhH_09wTFAAt': 'VUwR2ZW5qyKkef0sv02WwH_9cLRbcR9LS3HCOVzqi6EBU60gBpPWDNOvgdy8IyFo', 'zNUfdTb5_7vKBTluuEDLvuwvObOmAviowJFxey7EFMU0pyTlG0KR6Js5DeBjw5fk': 'FSGxW0Fzh6yOiMpoimqrd29fZRArYOD6y.D7i0SC.HMaop6_9OAzpVmz49KyCPYI', 'lQDRcJlnDLS0joEfC_X3rhgXuwL9d1h00A88jgn4CqgIG3bCc57bJaISDW8miEpx': 'urPJpAQ6xC7Svx_dVcflm2EL9_BGr8EAizmGUR.CDoq573pzo5E1OT6O4U1wfQum'}, 260488: 'WusXfkV3tUcmFEYSZYNYlzLxKqBCvsb0gtesCWYgp0KL5ikzlOW0VaIYUXYE1qZh', 933103: {'uh9XkHbkoXjPMfleM3FwUHg8E.LqKhSTIVSydNIDD.crGtvFIV4ZHFmOwc4uF2cF': 'X5ba_ErgZ56UPv_kGceeC7m0uSFisTnaL5Zsbm70SDq5184RNWtCYoMUmgb_3wf3', '6_yjO9FO.VlUKZCcSDabdAn15j1TrsEWQkI4mLAerCFjySe9arrf6bVeGZ0TpjR4': '697mVAfCoXJYASL93DvOyTYOdjuSNibBka37YSUfRXls_8mIKLiiMs2Q8mR4F1sb', '74lbQJMxvG5h5WneuHKWlMQVvLVMdCitudj8zYO4VBQMJJeR.HHYOrtpCUPkjlEj': 'uUvoNXPgrNadxjND0zX0lH3EcNx.nssGLhf9Qe3hsWVszazZ9AaCSot62N24iHrW', 'bZZ8H1z_G2CL_7AFIG9CsM6lIcleMn1Ue2beNboC8Kz_eAiObinlqlFe2g2h37kg': 'ycdoiPvz8dYohgNcZ5fCY8i8SK5emx3vGbqdGygNAJC9PWdduzgiN9y92ODaszjA', 'vzltF7gd5Q6FzGiZod1EVU_C7ZentSc.nBCkVj2Hlza1PpMcXK4ahcUdjnTPnzxm': 'symaE02yvTe2_g0ZlMneFoqJSywHmwa3gxPoUGq51DAgGBNuOV9txHSDvvJhzZ0Q', 'KrhK3UeVQNwzzOe1rLfPM9u7318jodxpISBABX4ZAbDuyP15CCLHDAwS2A3KycxI': {'_Rd.eqy_G5q4Qgv498XoE.4PWYH9IHG9WmbI6XW3ARiOWT07FoX.uf_2OF_IhuXZ': 'CRl.z6XvSkWAWLCtzUvzs6.bbGZgDbA_dHtxWZ3ui7JWU5y1dECYfSIt98cTBHAK', 'PEFRJ10h8T9IjEvlSj_bE4ARH5zxpvfG83zwMklqsEl_.FeHP.ZSK2ocEv7lH6SC': {206572: 'AX3.RAtGl2XdsBBw00lXdxEXkNT7tWtHmG8D4veho7Oou26FD.DejrG3Dyes1L3A', 36173: 'RYAiBpFIXROrJq2ysgYJS.zjV25ARVhhPKZhibmtdalu6X4PxoWlwlPGzcP5UkED', 176023: 'hhkGjaqIs1UA9VvdkfjJyf_IeQVFnH7pReBMBqo2ZHOj3y_KFOpXSspSnSJ9WN2f'}, 'dTr5yv1HGgeMhc8QhuyGwReFc5NHSEcFE0eX.SoFc3jbfXgCxzzKcK6zJyfYQAPL': 'pghQyBRVKrfm2h1SrK6gtSjGR7y0On74OqrCY7_C.GQHgNg18zXB2s7Up4TjA6Uw', 'F0afq_btHn1BrKRb43oNZBMpkg9x6d2SDPgFSqWglRsKv_YdGfLN8N8t4VJfMm33': '2dXwYcLFqgkP432eslzX8apmh4GapqvQbUa2D.eTs365_.SJjYQawPCBYx8NEx06', 'X5rRxxQTwC25jBt.G.iZ3KOoD8yCH9zw.9L1xmdaRBqt.GLNjiZxy6G.8RB9V8Hl': 'Uhgjgl58gKiVK2Viu.YBMFOe5fAy419VNbM_W9fGIOn6rz_b5NNERCFKN7wIAvL6', 'Ga6rFkg6SO._97vIgVtPzmR0KlWieEInYwtTgnooFQwVhaVakSm_IUm9NB78gP6b': 'eCEnQLh7WQzX1T6Gyei8tToYQuWfFOGG47iRaGNqnUh9tPftYWXa_I38.ZHR9In_'}}, 68595: 'fbAz6GQdCM_a1GqE3E_jDiWqFky34NF0FFZU8Q7CloLQ04w.DEY7qUPn38R5KCZa', 73077: {'uOI4t2xijl5uZDfI6m_ikZE6U76mQqjR61xw37EISo3Q_le7DqSrazYS2BamHEBe': 'NshxTFohLcxns9WfpMrjBMWxk3EZjdNIyHghmMyymiz4Wj89DCGiSlBfNKb9z1tG', 'PwIYQT7BhIVlFi_9zeeZUeqQ_Nnf4C7NTdUAwKxUw6KOUUpsKgRAg1mMdgpISb3v': 521470, 'xgHIRv7ObWNROUZPIr4nCJUW5lA_VRj5z2z5SrIJQJDRYn.wkZoRS0fvWh76BYkx': 'lhO.JLFGxM4IhQGA200f.cWqmcKafFosFK5kC6UvyZbWMlnEOVVJbqY_HieufgIq', '3xkz9lve6KHOxM.SDNOjz92wSdpowlJRC0t1MvOCpqRHOH23EhpHmFcJkndFOFPu': 'KQfwcG2how0dnsTmz4RvCNiZ.SrHdpkgTXbiF7G1xJ3NWyeWt7809ioe7GV6RxCo', 'xEjL_K_1xHd8fqU9_barbXEYfJCxuUUUzRapT6hUN6zRznYvYTRqiXNmZPqNsnIP': 'YL2.acNJwFJF1L.NOe8vgQZgi.PYcyFi5_IPt5YJZ7kryjAj9AOd0JAS6vyRYley'}, 135388: 'Bd6ezTM.UO.fRts3E4XeDSdJb4ffWjxAOcxAQptDo2S51iUk6lNxPs74okY3oiOD'}, 585070: 's5721kLqW.4WJUdK5Bg4BrgH_hEZbdHMhLKXvgeP3s.z3lGGz2FZgDsR9ce8wZob', 1007409: 'tfZTcGKvPll5kDI5Em.1dsfhNzCliRPe_3rtHwleSzotwb66AzTgZj1pIsOSMEdD', 427954: 'BLdewdg2j4BaokHt776w52iiO5IpQD_enLooH4ARfzeSV006O1bWXP1H_X42GWV2', 369812: 'JTG1rE1Hr1K8m6YlY1bYRvXptEYr.Q8z7OBNDWgkxZpfdIZMXN8DanDvMJKwTg4b', 805685: 'XYUMCQpSTELMwr9PeGbKrMlt.YIGWK02r_PNfQPESmjToVFAqJ_g8e5gvm3axnfP', 699455: {704704: 'G4NLv7V_rkc2dxdmNWD7vqI1O_5d.oVs8Z1bjju9H1cAlLXEYvTctC1V02EM4Q6M', 1040729: 'Yd_CLdBEFm7K0P80Jv6UylkvaDvt1_APH3gwKul_O1cLZN1qljkBPuipovYCv146', 238463: {'w5Qs5gmeIxf5pVZgZkNkzOmsD3V.I0SwxcT9_gQYfATvc1TPzOur3hQweG0ZpX6p': '.Q8OysixGYY_ZQft6.8KGLeJZ4eWO_Zc5fPmFbOe.zBsnYgwzkMQG1ejJa18G.Gh', 'uimdTaeNChBp07fi5kj2ssqhOD_i8OZLDLDTWgbTe3AWSjsc9eckJ1lA9zbulF_g': 'WSWedFJax37EXYcnuuO_Tg0HurkNl05K2aDlx0h0CaNrFX1ILeG24LjkSRMH85yC', 't33TgsYU1Z.8pka2Af4qXs29BPALEZUqDjp2pFdc4uukMEWFaUcVoPJymUs7qU.D': '6fzi4ywdJXA7pJp5glC83npQ0ft3XdiDLRrEi9yFPY.dLyszEXS6GeNjFCXn.KLZ', 'MqDacEFIsHzDhWh1EN8moFEIbEDZOO638WSJ2tcjMzq2BZXfNxrK0kc.NPRdugIM': 'laJnEo1LM2C4c7FEg6cjrLefKNrN5adAI8mLOnaz2Kr3yPtHdET2ScqYp03k9A1e', 'RQOa0qvz7cJE3STbK60T3xc0JXnbMLI011.JfLfpQDxCh5mE6qelKzLv.INaC6AN': 'CoQ2Mp4I00Geyjt.581jQqYZ0qRMpTJSs4hY58LgU.uR2i6izWTx7ml73KV2q5uK', 'G8QT2nYkqQIaMEFsMcjj4yP2GncNpjFh5ogz7h0YJ9SBGfCeRCD_KOcQ2A4FCAgC': 'NDEPgq_68Qu6y1ggwNILbR9hSOYeBlo3ze4LWOLsgaUgZx26ASAZ.2ozdVrgRSXw', 'cp05z3ixa5zE2CX49nEN1277Uzi6eNps7oAEQ3Ivxe9hMG_9tMM.xP_UagnxVt5L': 'UBlli_GbQq8Cba3LIF9XOsKfsB3UNeuKatdRJL9NPgg3LtglRGGRYpGdq3SfUutr'}}}",
    "example_output": "[['fbAz6GQdCM_a1GqE3E_jDiWqFky34NF0FFZU8Q7CloLQ04w.DEY7qUPn38R5KCZa', ['KQfwcG2how0dnsTmz4RvCNiZ.SrHdpkgTXbiF7G1xJ3NWyeWt7809ioe7GV6RxCo', 521470, 'NshxTFohLcxns9WfpMrjBMWxk3EZjdNIyHghmMyymiz4Wj89DCGiSlBfNKb9z1tG', 'YL2.acNJwFJF1L.NOe8vgQZgi.PYcyFi5_IPt5YJZ7kryjAj9AOd0JAS6vyRYley', 'lhO.JLFGxM4IhQGA200f.cWqmcKafFosFK5kC6UvyZbWMlnEOVVJbqY_HieufgIq'], 'Bd6ezTM.UO.fRts3E4XeDSdJb4ffWjxAOcxAQptDo2S51iUk6lNxPs74okY3oiOD', 'WusXfkV3tUcmFEYSZYNYlzLxKqBCvsb0gtesCWYgp0KL5ikzlOW0VaIYUXYE1qZh', ['VUwR2ZW5qyKkef0sv02WwH_9cLRbcR9LS3HCOVzqi6EBU60gBpPWDNOvgdy8IyFo', 'urPJpAQ6xC7Svx_dVcflm2EL9_BGr8EAizmGUR.CDoq573pzo5E1OT6O4U1wfQum', 'FSGxW0Fzh6yOiMpoimqrd29fZRArYOD6y.D7i0SC.HMaop6_9OAzpVmz49KyCPYI'], ['697mVAfCoXJYASL93DvOyTYOdjuSNibBka37YSUfRXls_8mIKLiiMs2Q8mR4F1sb', 'uUvoNXPgrNadxjND0zX0lH3EcNx.nssGLhf9Qe3hsWVszazZ9AaCSot62N24iHrW', ['2dXwYcLFqgkP432eslzX8apmh4GapqvQbUa2D.eTs365_.SJjYQawPCBYx8NEx06', 'eCEnQLh7WQzX1T6Gyei8tToYQuWfFOGG47iRaGNqnUh9tPftYWXa_I38.ZHR9In_', ['RYAiBpFIXROrJq2ysgYJS.zjV25ARVhhPKZhibmtdalu6X4PxoWlwlPGzcP5UkED', 'hhkGjaqIs1UA9VvdkfjJyf_IeQVFnH7pReBMBqo2ZHOj3y_KFOpXSspSnSJ9WN2f', 'AX3.RAtGl2XdsBBw00lXdxEXkNT7tWtHmG8D4veho7Oou26FD.DejrG3Dyes1L3A'], 'Uhgjgl58gKiVK2Viu.YBMFOe5fAy419VNbM_W9fGIOn6rz_b5NNERCFKN7wIAvL6', 'CRl.z6XvSkWAWLCtzUvzs6.bbGZgDbA_dHtxWZ3ui7JWU5y1dECYfSIt98cTBHAK', 'pghQyBRVKrfm2h1SrK6gtSjGR7y0On74OqrCY7_C.GQHgNg18zXB2s7Up4TjA6Uw'], 'ycdoiPvz8dYohgNcZ5fCY8i8SK5emx3vGbqdGygNAJC9PWdduzgiN9y92ODaszjA', 'X5ba_ErgZ56UPv_kGceeC7m0uSFisTnaL5Zsbm70SDq5184RNWtCYoMUmgb_3wf3', 'symaE02yvTe2_g0ZlMneFoqJSywHmwa3gxPoUGq51DAgGBNuOV9txHSDvvJhzZ0Q']], 'JTG1rE1Hr1K8m6YlY1bYRvXptEYr.Q8z7OBNDWgkxZpfdIZMXN8DanDvMJKwTg4b', 'BLdewdg2j4BaokHt776w52iiO5IpQD_enLooH4ARfzeSV006O1bWXP1H_X42GWV2', 's5721kLqW.4WJUdK5Bg4BrgH_hEZbdHMhLKXvgeP3s.z3lGGz2FZgDsR9ce8wZob', [['NDEPgq_68Qu6y1ggwNILbR9hSOYeBlo3ze4LWOLsgaUgZx26ASAZ.2ozdVrgRSXw', 'laJnEo1LM2C4c7FEg6cjrLefKNrN5adAI8mLOnaz2Kr3yPtHdET2ScqYp03k9A1e', 'CoQ2Mp4I00Geyjt.581jQqYZ0qRMpTJSs4hY58LgU.uR2i6izWTx7ml73KV2q5uK', 'UBlli_GbQq8Cba3LIF9XOsKfsB3UNeuKatdRJL9NPgg3LtglRGGRYpGdq3SfUutr', '6fzi4ywdJXA7pJp5glC83npQ0ft3XdiDLRrEi9yFPY.dLyszEXS6GeNjFCXn.KLZ', 'WSWedFJax37EXYcnuuO_Tg0HurkNl05K2aDlx0h0CaNrFX1ILeG24LjkSRMH85yC', '.Q8OysixGYY_ZQft6.8KGLeJZ4eWO_Zc5fPmFbOe.zBsnYgwzkMQG1ejJa18G.Gh'], 'G4NLv7V_rkc2dxdmNWD7vqI1O_5d.oVs8Z1bjju9H1cAlLXEYvTctC1V02EM4Q6M', 'Yd_CLdBEFm7K0P80Jv6UylkvaDvt1_APH3gwKul_O1cLZN1qljkBPuipovYCv146'], 'XYUMCQpSTELMwr9PeGbKrMlt.YIGWK02r_PNfQPESmjToVFAqJ_g8e5gvm3axnfP', 'tfZTcGKvPll5kDI5Em.1dsfhNzCliRPe_3rtHwleSzotwb66AzTgZj1pIsOSMEdD']",
    "inputs": map(lambda x: [dict_1_make(x[0])], random_number_list(1, 128, 10)),
    "success_hash": "41e5fdc9a6ee087d89abf07c7facde5cfc308174"
  },
  {
    "name": "socket-0",
    "description": "Connect to localhost on port 9999. You will receive two numbers in decimal notation separated by a comma. Add these two numbers together and return the result.",
    "example_input": "1234,5678",
    "example_output": "6912",
    "inputs": random_number_list(2, 128, 11),
    "success_hash": "a6f6350639f6e36ebfd5d73b0f1a95ae9e66579e",
    "special_solve_function": socket_0_solve
  },
  {
    "name": "socket-0",
    "description": "Connect to localhost on port 9999. You will receive a series of numbers in decimal notation separated by commas, terminated by a newline. Send the sum of these numbers in decimal notation. Continue doing this until you receive an empty line with trailing newline. Return the sum of all numbers received during this process.",
    "example_input": "N/A",
    "example_output": "N/A",
    "inputs": random_number_list(16, 128, 12),
    "success_hash": "9b6f632b0d3a2f9be6fe13bc091f9f8749303d01",
    "special_solve_function": socket_1_solve
  }
]

class CyberPythonEvaluator :
    def __init__ (self) :
        self.challenges = []
        for cd in challenge_data :
            special_solve_function = None
            if "special_solve_function" in cd :
                special_solve_function = cd["special_solve_function"]
            self.challenges.append(Challenge(name=cd["name"],
                                             description=cd["description"],
                                             example_input=cd["example_input"],
                                             example_output=cd["example_output"],
                                             inputs=cd["inputs"],
                                             success_hash=cd["success_hash"],
                                             special_solve_function=special_solve_function))

    def get_challenge (self, i) :
        return self.challenges[i]