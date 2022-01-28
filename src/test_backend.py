"""Test Script for RapMachineBackend"""



# import RapMachineBackendT5

# rm = RapMachineBackendT5.RapMachineT5(
#     '/home/philko/Documents/Uni/WiSe2122/CL/KuenstKrea/RapMachine/.model/T5-2-large', 'OffWords.txt')

# rm.load()
# generated = rm.generate(
#     ['compton', 'luck', 'gangsta', 'car', 'police', 'apple'], 4)
# ranked = rm.rank(generated)
# censored = list(map(lambda sent: rm.censor(sent), ranked))
# print(censored)


import RapMachineBackendGPT2

rm = RapMachineBackendGPT2.RapMachineGPT2(
    '/home/philko/Documents/Uni/WiSe2122/CL/KuenstKrea/RapMachine/.model/GPT2-2Ep', 'OffWords.txt')

rm.load()
generated = rm.generate(
    '@RapMachine7 Straignt', 4)
ranked = rm.rank(generated)
censored = list(map(lambda sent: rm.censor(sent), ranked))
print(censored)