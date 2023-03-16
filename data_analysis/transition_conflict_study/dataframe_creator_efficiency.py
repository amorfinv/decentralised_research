import config as cfg
from rich import print

import pandas as pd


flst_metrics = list(cfg.flst_metrics.keys())

new_flst_df_cols = ['density', 'concept', 'repetition'] + flst_metrics
new_flst_df = pd.DataFrame(columns=new_flst_df_cols)

rep_cols = ['ACID'] + [f'{concept}_{metric}' for concept in cfg.concepts_dict for metric in flst_metrics]
rep_eff_cols = [f'{concept}_{metric}_efficiency' for concept in cfg.concepts_dict for metric in flst_metrics]

for density, density_name in cfg.density_dict.items():


    for repetition in cfg.repetitions:

        # repetition_dataframe
        rep_df = pd.DataFrame(columns=rep_cols+rep_eff_cols)

        # get a list of acids in constrained
        acids_constrained = cfg.ac_in_constrained_dict[density][str(repetition)]['acids_in_constrained']
        sorted_acids = sorted(acids_constrained)
        
        # there are some small issues with the ultra_3 scenarios so remove some of these ACIDS
        if density == 'ultra' and repetition == 3:
            problematic_acids = ['D8222', 'D8198', 'D8129', 'D7585', 'D7698', 'D8016', 'D8429', 'D6316']
            
            for problem_acid in problematic_acids:
                sorted_acids.remove(problem_acid)

        # there are some small issues with the ultra_6 scenarios so remove some of these ACIDS
        if density == 'ultra' and repetition == 6:
            problematic_acids = ['D8110', 'D8003', 'D8221', 'D7586', 'D8236', 'D7908', 'D7910', 'D8083', 'D7978', 'D8085', 'D7360']
            
            for problem_acid in problematic_acids:
                sorted_acids.remove(problem_acid)

        rep_df['ACID'] = sorted_acids


        # first for loop 
        for concept, concept_name in cfg.concepts_dict.items():
            
            # get logs in a dataframe
            flst_log = f'{cfg.log_location}/FLSTLOG_Flight_intention_{density}_40_{repetition}_{concept}.log'
            flst_df = pd.read_csv(flst_log, skiprows=9, header=None, names=cfg.FLST_cols)

            # create a new column for those in constrained airspace
            flst_df['in_constrained'] = flst_df['ACID'].isin(sorted_acids)

            # only keep those in constrained
            df_filtered = flst_df[~(flst_df['in_constrained'] == False)]

            # sort the dataframe based on ACID and reset the index
            df_sorted = df_filtered.sort_values(by='ACID')
            df_sorted.reset_index(inplace=True)

            # now check that the order of acids is the same and has some data
            if df_sorted['ACID'].tolist() != sorted_acids:
                raise Exception(f'Dataframe does not match the aircraft in constrained for {flst_log}')

            for metric in flst_metrics:                
                # now assign the metric column
                rep_df[f'{concept}_{metric}'] = df_sorted[metric]


        # for each repetition calculate the efficiency
        for eff_metric in rep_eff_cols:
            # get the baseline metric
            metric = eff_metric.split('_')[1]
            baseline_metric = rep_df[f'noflow_{metric}']

            # get the concept metric
            concept_metric = rep_df['_'.join(eff_metric.split('_')[:2])]

            rep_df[eff_metric] = ((baseline_metric - concept_metric)/baseline_metric) * 100

        # now save in the dataframe
        for concept, concept_name in cfg.concepts_dict.items():
            
            
            
            # get conflict data in dataframe (percentages)
            flst_df_conf_scn = pd.DataFrame(
                [
                    [
                        density_name,
                        concept_name,
                        repetition,
                        *[rep_df[f'{concept}_{metric}_efficiency'].mean() for metric in flst_metrics]


                    ]
                ],
                columns=new_flst_df_cols
            )
            new_flst_df = pd.concat([new_flst_df, flst_df_conf_scn])

new_flst_df.to_csv('efficiency_df.csv', index=False)
