"""A short script to consolidate IFC text data for projects that 
were publicly disclosed. The data were manually downloaded from
IFC Disclosure Website: https://disclosures.ifc.org/

This script is intended to be used from a command line.
See usage in README.md
"""
import argparse
import sys
import os
from glob import glob
from datetime import date

import pandas as pd

COL_PID = 'Project Number'
COL_DOC_TYPE = 'Document Type Description'

def parse_arg():
    """Parse arguments from command line.

    Args:
        None

    Returns:
        project_type (string): a string indicating the type of projects to be
                               consolidated
    """
    desc = "Consolidate CSV files based on a specified IFC project type"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('type',
                        help='Type IS or AS')
    arg = parser.parse_args()

    if arg.type == 'IS':
        project_type = 'Investment'
    elif arg.type == 'AS':
        project_type = 'Advisory'
    else:
        print("please type the choice between IS and AS")
        sys.exit()
    return project_type


def consolidate_data(proj_type, target_dir):
    """Parse arguments from command line.

    Args:
        proj_type (string): a string indicating a project type
                            either 'Investment' or 'Advisory'
        target_dir (string): path to location where the consolidated data 
                             should be saved

    Returns:
        project_type (string): a string indicating the type of projects to be
                               consolidated
    """
    # part 3
    file_list = glob('*.csv')
    consolidated_df = pd.DataFrame()
    for file in file_list:
        cur_df = pd.read_csv(file, encoding='ISO-8859-1')
        consolidated_df = pd.concat([consolidated_df, cur_df], axis=0)
    consolidated_df.reset_index(drop=True, inplace=True)
    consolidated_df = consolidated_df.astype({COL_PID: 'string'})

    print('\nConsolidation is completed.\nExporting file...')

    # part 4
    today = date.today().strftime("%Y-%m-%d")
    output_name = f'{today} IFC_{proj_type}_disclosed_projects_text_data.csv'
    target_dir = os.path.join(os.getcwd(), 'Consolidated_data_set', 
                              output_name)
    consolidated_df.to_csv(target_dir, encoding='utf-8')

    print(f'\nExport is completed. The file is ready in {target_dir}\n')

    return consolidated_df


def process_investment_data(consolidated_df, target_dir, project_type):
    """If the project type is 'Investment', the data needs to be processed
    because the project ID is not unique in each row

    Args:
        proj_type (string): a string indicating a project type
                            either 'Investment' or 'Advisory'
        target_dir (string): path to location where the consolidated data 
                             should be saved

    Returns:
        project_type (string): a string indicating the type of projects to be
                               consolidated
    """
    # hard-coding column names in the next 4 lines
    first_text_col_idx = consolidated_df.columns.get_loc('Project Description')
    last_text_col_idx = consolidated_df.columns.get_loc('Mitigation Measures')
    project_id_col_idx = consolidated_df.columns.get_loc(COL_PID)
    unique_pid_row_df = consolidated_df.drop_duplicates(subset=COL_PID)
    
    unique_pid_row_df = unique_pid_row_df.drop(
                                unique_pid_row_df.iloc[:, first_text_col_idx:
                                                last_text_col_idx+1], axis=1)
    unique_pid_row_df = unique_pid_row_df.drop(columns=[COL_DOC_TYPE])
    # unique_pid_row_df has all attributes except text columns
    # next line hard-codes document type column name 
    distinct_doc_types = consolidated_df[COL_DOC_TYPE].unique().tolist()
    print("Available document types are: ")
    print('\n'.join(distinct_doc_types))
    for doc_type in distinct_doc_types:
        # add a prefix to text columns indicating which document type 
        # the text column is from
        col_prefix = '_'.join(doc_type.split()) + '_'
        cur_subset_df = consolidated_df.loc[
                                    consolidated_df[COL_DOC_TYPE] == doc_type]
        # create a text data subset which only has project ID 
        # and text columns for merging
        subset_index = [project_id_col_idx] + [j for j in range(
                                    first_text_col_idx, last_text_col_idx+1)]
        cur_subset_df = cur_subset_df.iloc[:, subset_index].add_prefix(
                                                                    col_prefix)
        cur_subset_df.rename(columns={f'{col_prefix}Project Number': COL_PID},
                                        inplace=True)

        # merge the subset with the main dataframe where row's PID is unique
        unique_pid_row_df = unique_pid_row_df.merge(cur_subset_df, on=COL_PID, 
                                                    how='left')
        unique_pid_row_df.reset_index(drop=True, inplace=True)

    unique_pid_row_df = unique_pid_row_df.dropna(axis='columns', how='all')

    print("\nExporting the consolidated file\n", 
          "each row has a unique project id...")
    today = date.today().strftime("%Y-%m-%d")
    output_name = f'{today} Unique_IFC_{project_type}_disclosed_projects_text_data.csv'
    target_dir = os.path.join(os.getcwd(), 
                             'Consolidated_data_set', output_name)
    unique_pid_row_df.to_csv(target_dir, encoding='ISO-8859-1')
    print(f'\nExport completed. The file is ready in {target_dir}\n')



def main():
    # part 1 Command line argument parsing
    project_type = parse_arg()
    print(f'IFC {project_type} Services was selected')
    print(f'\nConsolidating IFC {project_type} Services CSV files...')

    # part 2
    current_dir = os.getcwd()
    target_dir = os.path.join(current_dir, f'{project_type}_Services')
    os.chdir(target_dir)

    # part 3 & 4
    consolidated_df = consolidate_data(project_type, target_dir)

    # part 5
    if project_type == 'Investment':
        print(("\nFor investment projects, producing a data"
                "set where each row contains a unique project ID..."))
        process_investment_data(consolidated_df, target_dir, project_type)


if __name__ == '__main__':
    main()
