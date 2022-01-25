"""Test Script for RapMachineBackend"""



from src import RapMachineBackend

rm = RapMachineBackend.RapMachine(
    '/home/philko/Documents/Uni/WiSe2122/CL/KuenstKrea/RapMachine/.model/T5-1')

rm.load()
generated = rm.generate(
    ['compton', 'luck', 'gangsta', 'car', 'police', 'apple'], 4)
print(generated)
ranked = rm.rank(generated)
censored = rm.censor(ranked)