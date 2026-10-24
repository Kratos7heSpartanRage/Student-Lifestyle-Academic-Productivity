import pandas as pd
import numpy as np
import re

# Read raw
raw = pd.read_csv('raw_data.csv')
print('Raw shape:', raw.shape)

# Step 1: Standardize column names (aligned with Pranav and Krish)
# Let's map raw column names to concise, standard names
col_map = {
    'Timestamp': 'timestamp',
    'What is your current year of study?': 'year_of_study',
    'What is your gender? ': 'gender',
    'On average, how many days per week do you go to the gym or do structured workouts (weights, cardio, yoga, home workouts, walking or jogging)?': 'gym_days_per_week',
    'On average, how many hours per week do you play sports (cricket, football, badminton, etc.)?': 'sports_hours_per_week',
    'On average, how many hours do you sleep per night on weekdays?': 'sleep_hours',
    'At what time do you usually fall asleep on weekdays?': 'bedtime',
    'How would you rate your sleep quality over the past month?': 'sleep_quality',
    'Do you use your phone in the last 30 minutes before sleeping?': 'phone_before_sleep',
    'On average, how many hours per day do you spend on your phone/laptop for recreation (social media, videos, OTT, gaming, browsing)?': 'recreational_screen_hours',
    'Out of that, how many hours per day do you spend on social media (Instagram, YouTube Shorts, Snapchat, etc.)?': 'social_media_hours',
    'How many hours per day do you spend on gaming or OTT (Netflix, Prime, etc.)?': 'gaming_ott_hours',
    'How often do you get distracted by your phone while studying?': 'phone_distraction',
    'On average, how many hours per day do you spend studying outside class (including assignments and projects)?': 'study_hours',
    'How consistent are you in your study routine?': 'study_consistency',
    'What is your approximate class attendance?': 'class_attendance',
    'What is your latest SGPA/CGPA (out of 10)?': 'cgpa',
    'How would you rate your stress level during the last 4 weeks?': 'stress_level',
    'How well are you able to concentrate while studying?': 'concentration',
    'How productive do you feel in your academic work (completing tasks on time, understanding concepts)?': 'academic_productivity',
    'How often do you feel mentally tired or drained during the day?': 'mental_fatigue',
    'Do you feel that your physical activity (gym/sports) helps your studies?': 'physical_activity_impact'
}

df = raw.rename(columns=col_map)

# Step 2: Remove completely blank or unusable rows (where all answers are missing or outcomes missing)
row_missing = df.drop(columns=['timestamp']).isnull().sum(axis=1)
# Drop rows with >= 10 missing answers (empty submissions)
df = df[row_missing < 10].copy()
print('After dropping empty submissions:', df.shape)

# Step 3: Numeric extraction functions
def parse_hours(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().lower()
    if s in ['na', 'n/a', 'nan', 'null', 'none', '']:
        return np.nan
    nums = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', s)]
    if not nums:
        return np.nan
    # Midpoint if range like 5-6
    v = float(np.mean(nums[:2]))
    if 'min' in s and not re.search(r'hour|hr|\dh', s):
        v /= 60.0
    return v

for c in ['sleep_hours', 'recreational_screen_hours', 'social_media_hours', 'gaming_ott_hours', 'study_hours']:
    df[c] = df[c].map(parse_hours)

# Sports hours
df['sports_hours_per_week'] = df['sports_hours_per_week'].map(parse_hours)

# CGPA extraction
df['cgpa'] = pd.to_numeric(df['cgpa'].astype(str).str.extract(r'(\d+(?:\.\d+)?)')[0], errors='coerce')

# Plausibility bounds (replace impossible outliers with NaN, do not delete entire row)
plausibility = {
    'sleep_hours': (2, 14),
    'recreational_screen_hours': (0, 16),
    'social_media_hours': (0, 16),
    'gaming_ott_hours': (0, 16),
    'study_hours': (0, 14),
    'cgpa': (4.0, 10.0),
    'sports_hours_per_week': (0, 50)
}

for c, (lo, hi) in plausibility.items():
    bad = df[c].notna() & ~df[c].between(lo, hi)
    if bad.any():
        print(f'{c}: replaced {bad.sum()} impossible values with NaN: {df.loc[bad, c].tolist()}')
        df.loc[bad, c] = np.nan

# Clean categorical text and Likert ratings
likert_cols = ['sleep_quality', 'phone_distraction', 'study_consistency', 'stress_level', 'concentration', 'academic_productivity', 'mental_fatigue']
for c in likert_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Standardize text columns
df['gender'] = df['gender'].replace({'male': 'Male', 'female': 'Female'}).fillna('Prefer not to say')
df['year_of_study'] = df['year_of_study'].str.strip()

# Ordinal encodings
gym_map = {'0 days': 0.0, '1-2 days': 1.5, '3-4 days': 3.5, '5 or more days': 5.5}
df['workout_days_num'] = df['gym_days_per_week'].map(gym_map)

sports_map = {'0 hours': 0.0, '1-3 hours': 2.0, '4-6 hours': 5.0, '7 or more hours': 8.0}
# if sports_hours_per_week is already parsed as numeric, fillna from band if present
# Total activity = workout days (scaled) + sports hours
df['total_activity_score'] = df['workout_days_num'].fillna(0) + df['sports_hours_per_week'].fillna(0)

# Activity Level
df['activity_level'] = pd.cut(df['total_activity_score'], bins=[-1, 0.5, 4.0, 100], labels=['Inactive', 'Moderate', 'Active'])

# Sleep Group
df['sleep_group'] = pd.cut(df['sleep_hours'], bins=[0, 5.99, 8.0, 24.0], labels=['<6h', '6-8h', '8h+'])

# Screen Group
df['screen_group'] = pd.cut(df['recreational_screen_hours'], bins=[-1, 3.0, 6.0, 24.0], labels=['Low (<=3h)', 'Medium (3-6h)', 'High (>6h)'])

# Composite scores (Academic, Wellbeing, Focus)
df['academic_score'] = df[['academic_productivity', 'concentration']].mean(axis=1) / 5.0 * 100.0
# Reverse code stress and fatigue for wellbeing
df['stress_reversed'] = 6.0 - df['stress_level']
df['fatigue_reversed'] = 6.0 - df['mental_fatigue']
df['wellbeing_score'] = df[['stress_reversed', 'fatigue_reversed', 'sleep_quality']].mean(axis=1) / 5.0 * 100.0
df['distraction_reversed'] = 6.0 - df['phone_distraction']
df['focus_score'] = df[['concentration', 'distraction_reversed']].mean(axis=1) / 5.0 * 100.0

print('Final cleaned dataframe shape:', df.shape)
df.to_csv('cleaned_data.csv', index=False)
print('Successfully saved cleaned_data.csv!')
