from statistics import NormalDist
import scipy.stats as st
import numpy as np

# From https://www.reddit.com/r/berkeley/comments/kbvxd2/calculating_your_grade_in_cs70_and_other_curved/

def grade(percentile):
    if 0.95 <= percentile <= 100:
        return 'A+'
    elif 0.78 <= percentile <= 0.95:
        return 'A'
    elif 0.66 <= percentile <= 0.78:
        return 'A-'
    elif 0.43 <= percentile <= 0.66:
        return 'B+'
    elif 0.26 <= percentile <= 0.43:
        return 'B'
    elif 0.16 <= percentile <= 0.26:
        return 'B-'
    elif 0.11 <= percentile <= 0.16:
        return 'C+'
    elif 0.07 <= percentile <= 0.11:
        return 'C'
    elif 0.04 <= percentile <= 0.07:
        return 'C-'
    else:
        return 'F'

def grade_to_z(grade):
    grade = grade.strip().upper()
    # Percentiles pulled from Berkeley Time (historically accurate)
    grades_to_p = {'A+' : [0.95, 0.99], 'A' : [0.78, 0.95], 'A-' : [0.66, 0.78],
                'B+' : [0.43, 0.66], 'B' : [0.26, 0.43], 'B-' : [0.16, 0.26],
                'C+':[0.11, 0.16], 'C' : [0.07, 0.11], 'C-' : [0.04, 0.07],
                'F' : [0.01, 0.04]}

    if grade not in grades_to_p:
        print(f"You are actually trolling. {grade} is not a possible grade.")
        exit()
    else:
        percentile = grades_to_p[grade]
        lower_z = round(st.norm.ppf(percentile[0]), 2) # norm.ppf is inverse of norm.cdf
        upper_z = round(st.norm.ppf(percentile[1]), 2)
        return [lower_z, upper_z]

def mt1_zscore(raw_score):
    # Updated 7/17/22
    mean = 134.76
    std = 36.93
    return (raw_score - mean)/std

def avg_std(score1, score2):
    return (score1 + score2)/2

def grade_to_percentile(grade):
    grade = grade.strip().upper()
    # Percentiles pulled from Berkeley Time (historically accurate)
    grades_to_p = {'A+' : [0.95, 0.99], 'A' : [0.78, 0.95], 'A-' : [0.66, 0.78],
                'B+' : [0.43, 0.66], 'B' : [0.26, 0.43], 'B-' : [0.16, 0.26],
                'C+':[0.11, 0.16], 'C' : [0.07, 0.11], 'C-' : [0.04, 0.07],
                'F' : [0.01, 0.04]}
    return grades_to_p[grade]

def predict_final_std_range(grade, z_score_MT):
    grade_range = grade_to_z(grade)
    lower = predict_final_std_exact(grade_range[0], z_score_MT)
    upper = predict_final_std_exact(grade_range[1], z_score_MT)
    print(f'Midterm 1 std: {round(z_score_MT, 2)}')
    print(f'To get an {grade}, you need to get a final std between ({lower},{upper}) based on past data.')

def predict_final_std_exact(desired_percentile, z_score_MT):
    for z_score_F in np.arange(-3, 3, 0.001):
        clobber = avg_std(z_score_MT, z_score_F)
        delta = 0.001

        # overall_std = sqrt([0.375 * std_m]^2 + [0.5 * std_f]^2 + 2 * 0.8 * 0.375 * 0.5 * std_m * std_f)
        # Where std_m and std_f are 1 since normal dist.
        overall_std = np.sqrt(0.375**2 + 0.5**2 + 2 * 0.8 * 0.375 * 0.5)
        percentile = NormalDist(mu=0, sigma=overall_std).cdf(0.375 * max(z_score_MT, clobber) + 0.5 * z_score_F) 
        
        if abs(percentile - desired_percentile) <= delta:
            return np.round(z_score_F, 2)

def predict_final_std_all(z_score_MT):
    grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'F']
    print(f'Midterm 1 std: {round(z_score_MT, 2)}')
    print(f'Here are all the final std ranges you need to hit to reach a certain grade:')
    for grade in grades:
        grade_range = grade_to_percentile(grade)
        lower = predict_final_std_exact(grade_range[0], z_score_MT)
        upper = predict_final_std_exact(grade_range[1], z_score_MT)
        
        if not upper and not lower:
            print(f"{grade}: Probabilistically Impossible")
        else: 
            print(f'{grade}: ({"Probabilistically Impossible" if not lower else lower},{"Probabilistically Impossible" if not upper else upper})')

if __name__ == "__main__":
    # calling the main function
    predict_final_std_all(mt1_zscore(float(input("Enter midterm 1 raw score: "))))
