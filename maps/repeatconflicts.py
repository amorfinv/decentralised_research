

import matplotlib.pyplot as plt
filenames = [
    'results/CONFLOG_Flight_intention_low_40_0_noflowrandomalloc.log',
# 'results/CONFLOG_Flight_intention_low_40_0_noflowfulldenalloc.log',
'results/CONFLOG_Flight_intention_low_40_0_m2.log',
]

names = ['randomalloc', 
# 'fulldenalloc', 
'm2']

fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

# We can set the number of bins with the *bins* keyword argument.
for idx, filename in enumerate(filenames):

    with open(filename, 'r') as f:
        lines = f.readlines()[9:]


    count_dict = {}

    for line in lines:

        list_acids = line.split(',')[1:3]
        list_acids.sort()
        acids = tuple(list_acids)

        if acids in count_dict:
            count_dict[acids] += 1

        else:
            count_dict[acids] = 1


    sorted_values = list(count_dict.values())
    sorted_values.sort()


    axs.hist(sorted_values, bins=120, label=names[idx])
    axs.set_ylim([0, 50])

leg = axs.legend()
plt.show()
plt.close()
    