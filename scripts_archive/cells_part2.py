import nbformat as nbf

cells_2 = []

# --- Unit 3: Normalization ---
cells_2.append(nbf.v4.new_markdown_cell(r"""## 4. Normalization Techniques: Raw vs Min-Max Scaling vs Z-Score Standardization (Unit 3)

In **Unit 3 (Data Normalization & Outliers)**, transforming continuous features onto standardized scales is essential before comparative analysis or gradient-based modeling:
1. **Min-Max Normalization (Feature Scaling):**
   $$x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}} \in [0, 1]$$
   - Preserves exact relationships and relative distances.
   - Bounds values strictly between 0 and 1. Highly sensitive to extreme outliers because $x_{\min}$ and $x_{\max}$ anchor the boundaries.
2. **Z-Score Normalization (Standardization):**
   $$z = \frac{x - \mu}{\sigma} \sim \mathcal{N}(0, 1)$$
   - Rescales the variable to have zero mean ($\mu=0$) and unit standard deviation ($\sigma=1$).
   - Does not bind values to a fixed interval; measures distance from the central tendency in terms of standard deviations. Robust to moderate variance shifts.
"""))

cells_2.append(nbf.v4.new_code_cell(r"""# 4.1 Normalization Demonstration and Visual Comparison (Unit 3)
norm_cols = ['study_hours', 'sleep_hours', 'recreational_screen_hours', 'cgpa']
norm_df = df[norm_cols].dropna().copy()

scaler_minmax = MinMaxScaler()
scaler_z = StandardScaler()

scaled_minmax = pd.DataFrame(scaler_minmax.fit_transform(norm_df), columns=[c + '_minmax' for c in norm_cols])
scaled_z = pd.DataFrame(scaler_z.fit_transform(norm_df), columns=[c + '_z' for c in norm_cols])

# Comparison Plot: 3 Rows (Raw, Min-Max, Z-score) x 4 Columns (Variables)
fig, axes = plt.subplots(3, 4, figsize=(16, 9))
palette_colors = ['#2563EB', '#059669', '#DC2626', '#7C3AED']

for j, col in enumerate(norm_cols):
    # Row 0: Original Raw Units
    sns.histplot(norm_df[col], kde=True, ax=axes[0, j], color=palette_colors[j], bins=10)
    axes[0, j].set_title(f'Raw: {col}\nMean={norm_df[col].mean():.2f}, Std={norm_df[col].std():.2f}')
    axes[0, j].set_xlabel('')
    
    # Row 1: Min-Max Normalized [0, 1]
    sns.histplot(scaled_minmax[col + '_minmax'], kde=True, ax=axes[1, j], color=palette_colors[j], bins=10)
    axes[1, j].set_title(f'Min-Max: {col}\nRange=[0.0, 1.0]')
    axes[1, j].set_xlabel('')
    
    # Row 2: Z-Score Standardized (Mean=0, Std=1)
    sns.histplot(scaled_z[col + '_z'], kde=True, ax=axes[2, j], color=palette_colors[j], bins=10)
    axes[2, j].set_title(f'Z-Score: {col}\nMean={scaled_z[col + "_z"].mean():.2f}, Std={scaled_z[col + "_z"].std():.2f}')
    axes[2, j].set_xlabel('Standard Deviations (z)')

axes[0, 0].set_ylabel('Raw Frequency')
axes[1, 0].set_ylabel('Min-Max Density')
axes[2, 0].set_ylabel('Z-Score Density')

plt.suptitle('Unit 3: Normalization Techniques — Comparing Raw vs Min-Max [0, 1] vs Z-Score Standardization', fontsize=14, y=1.02)
plt.tight_layout()
fig.savefig('figures_eda/eda_fig02_normalization_comparison.png', bbox_inches='tight')
plt.show()
print("Figure 2 generated and saved successfully.")
"""))

# --- Unit 3: Outliers & Leverage ---
cells_2.append(nbf.v4.new_markdown_cell(r"""## 5. Outliers, Leverage & Influential Points Analysis (Unit 3)

In accordance with **Unit 3 (Outliers, Leverage and Influential Points)**:
1. **Univariate Outliers:**
   - Evaluated using **Tukey's Fences**:
     $$\text{Lower Fence} = Q_1 - 1.5 \times IQR, \quad \text{Upper Fence} = Q_3 + 1.5 \times IQR$$
2. **Multivariate Leverage ($h_{ii}$):**
   - Derived from the diagonals of the projection Hat Matrix: $H = X(X^TX)^{-1}X^T$.
   - Quantifies the geometric extremity of an observation in the predictor predictor space.
   - Common heuristic threshold: $h_{ii} > \frac{2(p+1)}{n}$, where $p$ is the number of predictors and $n$ is sample size.
3. **Influential Points (Cook's Distance $D_i$):**
   - Measures aggregate change in fitted values when observation $i$ is deleted:
     $$D_i = \frac{\sum_{j=1}^n (\hat{y}_j - \hat{y}_{j(i)})^2}{(p+1) \cdot s^2}$$
   - Cut-off threshold: $D_i > \frac{4}{n}$ (or $D_i > 1.0$ for extreme distortion).
4. **Studentized Residuals ($r_i$):**
   - Residual divided by its estimated standard error ($r_i = \frac{e_i}{s_{(i)}\sqrt{1 - h_{ii}}}$). Observations with $|r_i| > 2$ or $3$ are potential response outliers.
"""))

cells_2.append(nbf.v4.new_code_cell(r"""# 5.1 Outliers, Leverage, and Cook's Distance Diagnostic Suite (Unit 3)
reg_subset = df[['study_hours', 'sleep_hours', 'recreational_screen_hours', 'cgpa']].dropna().copy()
X_diag = sm.add_constant(reg_subset[['study_hours', 'sleep_hours', 'recreational_screen_hours']])
y_diag = reg_subset['cgpa']

ols_model = sm.OLS(y_diag, X_diag).fit()
influence = ols_model.get_influence()

cooks_d = influence.cooks_distance[0]
leverage = influence.hat_matrix_diag
student_resid = influence.resid_studentized_internal
n_obs = len(reg_subset)
p_preds = 3
cooks_cutoff = 4.0 / n_obs
leverage_cutoff = 2.0 * (p_preds + 1) / n_obs

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# --- Panel 1: Tukey IQR Univariate Outlier Boxplots ---
ax = axes[0, 0]
sns.boxplot(data=df[norm_cols], ax=ax, palette='Set2')
ax.set_title('Univariate Outlier Detection (Tukey 1.5*IQR Rule)')
ax.set_ylabel('Feature Value (Original Units)')
ax.tick_params(axis='x', rotation=15)

# --- Panel 2: Cook's Distance Stem Plot ---
ax = axes[0, 1]
ax.stem(range(n_obs), cooks_d, markerfmt='ro', linefmt='r-', basefmt='k-')
ax.axhline(cooks_cutoff, color='#2563EB', linestyle='--', linewidth=1.5, label=f'Threshold (4/n = {cooks_cutoff:.3f})')
high_influence = np.where(cooks_d > cooks_cutoff)[0]
for idx in high_influence:
    ax.annotate(f'#{idx}', (idx, cooks_d[idx]), textcoords='offset points', xytext=(0, 6), ha='center', fontsize=8, fontweight='bold')
ax.set_title("Cook's Distance Plot (Influential Cases)")
ax.set_xlabel('Observation Index')
ax.set_ylabel("Cook's Distance (Di)")
ax.legend(frameon=True)

# --- Panel 3: Studentized Residuals vs Leverage ---
ax = axes[1, 0]
ax.scatter(leverage, student_resid, color='#4F46E5', alpha=0.7, edgecolors='black', s=50)
ax.axhline(2, color='red', linestyle=':')
ax.axhline(-2, color='red', linestyle=':')
ax.axvline(leverage_cutoff, color='#059669', linestyle='--', linewidth=1.5, label=f'Leverage Cutoff (2(p+1)/n = {leverage_cutoff:.2f})')
ax.set_title('Residuals vs Leverage Plot')
ax.set_xlabel('Leverage (hii, Hat Matrix Diagonals)')
ax.set_ylabel('Studentized Residuals')
ax.legend(frameon=True)

# --- Panel 4: Normal Q-Q Plot of Residuals ---
ax = axes[1, 1]
stats.probplot(ols_model.resid, dist='norm', plot=ax)
ax.set_title('Normal Q-Q Plot of OLS Residuals')
ax.get_lines()[0].set_markerfacecolor('#0D9488')
ax.get_lines()[0].set_markeredgecolor('black')
ax.get_lines()[1].set_color('#DC2626')

plt.suptitle('Unit 3: Diagnostic Analysis of Outliers, Leverage, and Influential Points', fontsize=14, y=1.02)
plt.tight_layout()
fig.savefig('figures_eda/eda_fig03_outliers_leverage_cooks.png', bbox_inches='tight')
plt.show()
print(f"Diagnosed {len(high_influence)} observations exceeding Cook's distance threshold (4/n = {cooks_cutoff:.3f}).")
"""))

# --- Unit 2 & 5: Categorical Analysis ---
cells_2.append(nbf.v4.new_markdown_cell(r"""## 6. Categorical Data Analysis & Contingency Tables (Unit 2 & 5)

In **Unit 2 (Categorical Data Analysis)** and **Unit 5 (Visualization for Categorical Variables)**:
1. **Contingency Tables ($r \times c$):** Cross-classifying frequencies across two qualitative or discretized attributes.
2. **Pearson's Chi-Square Test of Independence:**
   $$\chi^2 = \sum_{i=1}^r \sum_{j=1}^c \frac{(O_{ij} - E_{ij})^2}{E_{ij}} \sim \chi^2_{(r-1)(c-1)}$$
   - Null Hypothesis ($H_0$): The row attribute and column attribute are independent.
3. **Cramér's V (Effect Size):**
   $$V = \sqrt{\frac{\chi^2}{n \cdot \min(r-1, c-1)}} \in [0, 1]$$
   - $V < 0.10$: Negligible association; $0.10 - 0.30$: Moderate association; $> 0.30$: Strong association.
"""))

cells_2.append(nbf.v4.new_code_cell(r"""# 6.1 Contingency Tables, Chi-Square Tests & Stacked Visualizations (Unit 2 & 5)
def test_categorical_association(row_col, col_col):
    ct = pd.crosstab(df[row_col], df[col_col])
    chi2, p_val, dof, _ = stats.chi2_contingency(ct)
    n = ct.sum().sum()
    min_dim = min(ct.shape[0] - 1, ct.shape[1] - 1)
    cramer_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
    return ct, chi2, p_val, cramer_v

ct1, chi2_1, p_1, v_1 = test_categorical_association('phone_before_sleep', 'sleep_quality')
ct2, chi2_2, p_2, v_2 = test_categorical_association('screen_group', 'phone_distraction')
ct3, chi2_3, p_3, v_3 = test_categorical_association('activity_level', 'study_consistency')

print(f"1. Phone Before Sleep vs Sleep Quality: Chi2={chi2_1:.2f}, p={p_1:.4f}, Cramer's V={v_1:.3f}")
print(f"2. Screen Time Group vs Phone Distraction: Chi2={chi2_2:.2f}, p={p_2:.4f}, Cramer's V={v_2:.3f}")
print(f"3. Physical Activity Level vs Study Consistency: Chi2={chi2_3:.2f}, p={p_3:.4f}, Cramer's V={v_3:.3f}")

# Visualization: 1 Row x 3 Columns of Stacked Percentage Bar Charts
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Bedtime Phone Use vs Sleep Quality
(ct1.div(ct1.sum(axis=1), axis=0) * 100).plot(kind='bar', stacked=True, ax=axes[0], colormap='viridis', edgecolor='black')
axes[0].set_title(f'Bedtime Phone vs Sleep Quality\n(Chi2={chi2_1:.1f}, p={p_1:.3f}, V={v_1:.2f})')
axes[0].set_xlabel('Uses Phone Last 30 Mins Before Sleep')
axes[0].set_ylabel('Proportion (%)')
axes[0].legend(title='Sleep Quality', bbox_to_anchor=(1, 1))
axes[0].tick_params(axis='x', rotation=0)

# Plot 2: Screen Group vs Phone Distraction
(ct2.div(ct2.sum(axis=1), axis=0) * 100).plot(kind='bar', stacked=True, ax=axes[1], colormap='mako', edgecolor='black')
axes[1].set_title(f'Screen Time Group vs Distraction\n(Chi2={chi2_2:.1f}, p={p_2:.3f}, V={v_2:.2f})')
axes[1].set_xlabel('Recreational Screen Group')
axes[1].set_ylabel('Proportion (%)')
axes[1].legend(title='Distraction (1-5)', bbox_to_anchor=(1, 1))
axes[1].tick_params(axis='x', rotation=0)

# Plot 3: Activity Level vs Consistency
(ct3.div(ct3.sum(axis=1), axis=0) * 100).plot(kind='bar', stacked=True, ax=axes[2], colormap='flare', edgecolor='black')
axes[2].set_title(f'Physical Activity vs Consistency\n(Chi2={chi2_3:.1f}, p={p_3:.3f}, V={v_3:.2f})')
axes[2].set_xlabel('Physical Activity Level')
axes[2].set_ylabel('Proportion (%)')
axes[2].legend(title='Consistency (1-5)', bbox_to_anchor=(1, 1))
axes[2].tick_params(axis='x', rotation=0)

plt.suptitle('Unit 2 & 5: Categorical Data Analysis & Stacked Percentage Visualizations', fontsize=14, y=1.03)
plt.tight_layout()
fig.savefig('figures_eda/eda_fig05_categorical_crosstabs.png', bbox_inches='tight')
plt.show()
"""))

# --- Unit 5: Multi-layer Distributions ---
cells_2.append(nbf.v4.new_markdown_cell(r"""## 7. Exploratory Graphical Analysis: Continuous & Categorical Distributions (Unit 5)

In **Unit 5 (Exploratory Graphical Analysis)**, combining multiple visual layers prevents visual over-simplification:
- **Violin Plots:** Display kernel probability density estimates across groupings.
- **Embedded Boxplots:** Reveal the 5-number summary (Quartiles $Q_1, Q_2, Q_3$ and whiskers).
- **Overlaid Stripplots:** Render raw individual student data points, preserving micro-level variability and revealing sample density.
"""))

cells_2.append(nbf.v4.new_code_cell(r"""# 7.1 Multi-Layered Exploratory Graphical Analysis (Unit 5)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Subplot 1: Physical Activity Level vs Stress
ax = axes[0, 0]
sub_act = df.dropna(subset=['activity_level', 'stress_level'])
sns.violinplot(data=sub_act, x='activity_level', y='stress_level', hue='activity_level', legend=False, ax=ax, palette='Blues', inner=None, cut=0)
sns.boxplot(data=sub_act, x='activity_level', y='stress_level', ax=ax, width=0.22, color='white', showcaps=True)
sns.stripplot(data=sub_act, x='activity_level', y='stress_level', ax=ax, color='black', alpha=0.5, jitter=0.2, size=5)
ax.set_title('Physical Activity Level vs Self-Rated Stress')
ax.set_xlabel('Activity Category')
ax.set_ylabel('Stress Rating (1=Low, 5=High)')

# Subplot 2: Sleep Group vs Concentration
ax = axes[0, 1]
sub_slp = df.dropna(subset=['sleep_group', 'concentration'])
sns.violinplot(data=sub_slp, x='sleep_group', y='concentration', hue='sleep_group', legend=False, ax=ax, palette='Purples', inner=None, cut=0)
sns.boxplot(data=sub_slp, x='sleep_group', y='concentration', ax=ax, width=0.22, color='white')
sns.stripplot(data=sub_slp, x='sleep_group', y='concentration', ax=ax, color='black', alpha=0.5, jitter=0.2, size=5)
ax.set_title('Sleep Duration Group vs Concentration Ability')
ax.set_xlabel('Weekday Sleep Group')
ax.set_ylabel('Concentration Rating (1-5)')

# Subplot 3: Screen Group vs Academic Productivity
ax = axes[1, 0]
sub_scr = df.dropna(subset=['screen_group', 'academic_productivity'])
sns.violinplot(data=sub_scr, x='screen_group', y='academic_productivity', hue='screen_group', legend=False, ax=ax, palette='Oranges', inner=None, cut=0)
sns.boxplot(data=sub_scr, x='screen_group', y='academic_productivity', ax=ax, width=0.22, color='white')
sns.stripplot(data=sub_scr, x='screen_group', y='academic_productivity', ax=ax, color='black', alpha=0.5, jitter=0.2, size=5)
ax.set_title('Screen Time Group vs Academic Productivity')
ax.set_xlabel('Recreational Screen Group')
ax.set_ylabel('Productivity Rating (1-5)')

# Subplot 4: Study Consistency vs CGPA
ax = axes[1, 1]
sub_cns = df.dropna(subset=['study_consistency', 'cgpa'])
sns.boxplot(data=sub_cns, x='study_consistency', y='cgpa', hue='study_consistency', legend=False, ax=ax, palette='Greens')
sns.stripplot(data=sub_cns, x='study_consistency', y='cgpa', ax=ax, color='black', alpha=0.6, jitter=0.2, size=6)
ax.set_title('Study Routine Consistency vs CGPA')
ax.set_xlabel('Consistency Rating (1=Irregular, 5=Highly Consistent)')
ax.set_ylabel('Latest CGPA (out of 10)')

plt.suptitle('Unit 5: Exploratory Graphical Distributions (Violin + Box + Strip Composites)', fontsize=14, y=1.02)
plt.tight_layout()
fig.savefig('figures_eda/eda_fig04_descriptive_distributions.png', bbox_inches='tight')
plt.show()
"""))

print("cells_part2 ready with", len(cells_2), "cells.")
