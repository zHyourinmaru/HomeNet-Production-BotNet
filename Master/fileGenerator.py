
class CreateTxt:

    def __init__(self):
        self.create()

    def create(sentence):
        f = open('botInformation.txt', 'w')
        sentence = sentence.split('#')
        i = 0

        with open('botInformation.txt', 'w') as f:
            f.write('=================================================================================================')
            f.write('\nSystem used:\t')
            f.write(str(sentence[0]))
            f.write('\nAccount name:\t')
            f.write(str(sentence[1]))
            f.write('\nRelease:\t')
            f.write(str(sentence[2]))
            f.write('\nVersion:\t')
            f.write(str(sentence[3]))
            f.write('\nMachine:\t')
            f.write(str(sentence[4]))
            f.write('\n=================================================================================================')
            f.write('\nProcessor:\t')
            f.write(str(sentence[5]))
            f.write('\nNumber of physical cores:\t')
            f.write(str(sentence[6]))
            f.write('\nTotal cores:\t')
            f.write(str(sentence[7]))
            f.write('\nMax frequency cores:\t')
            f.write(str(sentence[8]))
            f.write('\nMin frequency cores:\t')
            f.write(str(sentence[9]))
            f.write('\nCurrent frequency cores:\t')
            f.write(str(sentence[10]))
            f.write('\n=================================================================================================')
            f.write('\nBoot time:\t')
            f.write(str(sentence[11]))

