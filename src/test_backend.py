"""Test Script for RapMachineBackend"""



# from src import RapMachineBackendT5

# rm = RapMachineBackendT5.RapMachineT5(
#     '/home/philko/Documents/Uni/WiSe2122/CL/KuenstKrea/RapMachine/.model/T5-1', 'OffWords.txt')

# rm.load()
# generated = rm.generate(
#     ['compton', 'luck', 'gangsta', 'car', 'police', 'apple'], 4)
# print(generated)
# ranked = rm.rank(generated[0])
# censored = rm.censor(ranked)
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
for i in censored:
    print(len(i))