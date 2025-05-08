from django.db import models

## add sorting field "how do you want to sort multiple quantitative responses?"
## What is numeric value for this cause treatment?
## collapse response measure fields

# study metadata choices
study_type_choices = (
    ("Observational/gradient", "Observational/gradient"),
    ("Manipulation/experiment", "Manipulation/experiment"),
    ("Simulation", "Simulation"),
    ("Meta-analysis", "Meta-analysis"),
    ("Review", "Review"),
)
study_setting_choices = (
    ("Field", "Field"),
    ("Mesocosm", "Mesocosm"),
    ("Greenhouse", "Greenhouse"),
    ("Laboratory", "Laboratory"),
    ("Model", "Model"),
    ("Not applicable", "Not applicable"),
)
country_choices = (
    ("United States", "United States"),
    ("Afghanistan", "Afghanistan"),
    ("Albania", "Albania"),
    ("Algeria", "Algeria"),
    ("American Somoa", "American Somoa"),
    ("Andorra", "Andorra"),
    ("Angola", "Angola"),
    ("Anguilla", "Anguilla"),
    ("Antarctica", "Antarctica"),
    ("Antigua and Barbuda", "Antigua and Barbuda"),
    ("Argentina", "Argentina"),
    ("Armenia", "Armenia"),
    ("Aruba", "Aruba"),
    ("Australia", "Australia"),
    ("Austria", "Austria"),
    ("Azerbaijjan", "Azerbaijjan"),
    ("Bahamas", "Bahamas"),
    ("Bahrain", "Bahrain"),
    ("Bangladesh", "Bangladesh"),
    ("Barbados", "Barbados"),
    ("Belarus", "Belarus"),
    ("Belgium", "Belgium"),
    ("Belize", "Belize"),
    ("Benin", "Benin"),
    ("Bermuda", "Bermuda"),
    ("Bhutan", "Bhutan"),
    ("Bolivia", "Bolivia"),
    ("Bosnia and Herzegovina", "Bosnia and Herzegovina"),
    ("Botswana", "Botswana"),
    ("Brazil", "Brazil"),
    ("British Virgin Islands", "British Virgin Islands"),
    ("Brunei Darussalam", "Brunei Darussalam"),
    ("Bulgaria", "Bulgaria"),
    ("Burkina Faso", "Burkina Faso"),
    ("Burundi", "Burundi"),
    ("Cambodia", "Cambodia"),
    ("Cameroon", "Cameroon"),
    ("Canada", "Canada"),
    ("Cape Verde", "Cape Verde"),
    ("Cayman Islands", "Cayman Islands"),
    ("Central African Republic", "Central African Republic"),
    ("Chad", "Chad"),
    ("Chile", "Chile"),
    ("China", "China"),
    ("Colombia", "Colombia"),
    ("Comoros", "Comoros"),
    ("Congo", "Congo"),
    ("Cook Islands", "Cook Islands"),
    ("Costa Rica", "Costa Rica"),
    ("Cote d'Ivoire", "Cote d'Ivoire"),
    ("Croatia", "Croatia"),
    ("Cuba", "Cuba"),
    ("Cyprus", "Cyprus"),
    ("Czech Republic", "Czech Republic"),
    ("Democratic Republic of Congo", "Democratic Republic of Congo"),
    ("Denmark", "Denmark"),
    ("Djibouti", "Djibouti"),
    ("Dominica", "Dominica"),
    ("Dominican Republic", "Dominican Republic"),
    ("East Timor", "East Timor"),
    ("Ecuador", "Ecuador"),
    ("Egypt", "Egypt"),
    ("El Salvador", "El Salvador"),
    ("Equatorial Guinea", "Equatorial Guinea"),
    ("Eritrea", "Eritrea"),
    ("Estonia", "Estonia"),
    ("Ethiopia", "Ethiopia"),
    ("Falkland Islands", "Falkland Islands"),
    ("Faroe Islands", "Faroe Islands"),
    ("Fiji", "Fiji"),
    ("Finland", "Finland"),
    ("France", "France"),
    ("French Guiana", "French Guiana"),
    ("French Polynesia", "French Polynesia"),
    ("Gabon", "Gabon"),
    ("Gambia", "Gambia"),
    ("Georgia", "Georgia"),
    ("Germany", "Germany"),
    ("Ghana", "Ghana"),
    ("Gibraltar", "Gibraltar"),
    ("Greece", "Greece"),
    ("Greenland", "Greenland"),
    ("Grenada", "Grenada"),
    ("Guadeloupe", "Guadeloupe"),
    ("Guam", "Guam"),
    ("Guatemala", "Guatemala"),
    ("Guinea", "Guinea"),
    ("Guinea Bissau", "Guinea Bissau"),
    ("Guyana", "Guyana"),
    ("Haiti", "Haiti"),
    ("Honduras", "Honduras"),
    ("Hungary", "Hungary"),
    ("Iceland", "Iceland"),
    ("India", "India"),
    ("Indonesia", "Indonesia"),
    ("Iran", "Iran"),
    ("Iraq", "Iraq"),
    ("Ireland", "Ireland"),
    ("Israel", "Israel"),
    ("Italy", "Italy"),
    ("Jamaica", "Jamaica"),
    ("Japan", "Japan"),
    ("Jordan", "Jordan"),
    ("Kazakhstan", "Kazakhstan"),
    ("Kenya", "Kenya"),
    ("Kiribati", "Kiribati"),
    ("Kuwait", "Kuwait"),
    ("Kyrgyzstan", "Kyrgyzstan"),
    ("Laos", "Laos"),
    ("Latvia", "Latvia"),
    ("Lebanon", "Lebanon"),
    ("Lesotho", "Lesotho"),
    ("Liberia", "Liberia"),
    ("Libya", "Libya"),
    ("Liechtenstein", "Liechtenstein"),
    ("Lithuania", "Lithuania"),
    ("Luxembourg", "Luxembourg"),
    ("Macau", "Macau"),
    ("Macedonia", "Macedonia"),
    ("Madagascar", "Madagascar"),
    ("Malawi", "Malawi"),
    ("Malaysia", "Malaysia"),
    ("Maldives", "Maldives"),
    ("Mali ", "Mali "),
    ("Malta", "Malta"),
    ("Marshall Islands", "Marshall Islands"),
    ("Martinique", "Martinique"),
    ("Mauritania", "Mauritania"),
    ("Mauritius", "Mauritius"),
    ("Mayotte", "Mayotte"),
    ("Mexico", "Mexico"),
    ("Micronesia", "Micronesia"),
    ("Moldova", "Moldova"),
    ("Monaco", "Monaco"),
    ("Mongolia", "Mongolia"),
    ("Montserrat", "Montserrat"),
    ("Morroco", "Morroco"),
    ("Mozambique", "Mozambique"),
    ("Myanmar", "Myanmar"),
    ("Namibia", "Namibia"),
    ("Nauru", "Nauru"),
    ("Nepal", "Nepal"),
    ("Netherlands", "Netherlands"),
    ("Netherlands Antilles", "Netherlands Antilles"),
    ("New Caledonia", "New Caledonia"),
    ("New Zealand", "New Zealand"),
    ("Nicaragua", "Nicaragua"),
    ("Niger", "Niger"),
    ("Nigeria", "Nigeria"),
    ("Niue", "Niue"),
    ("Norfolk Island", "Norfolk Island"),
    ("North Korea", "North Korea"),
    ("Northern Mariana Islands", "Northern Mariana Islands"),
    ("Norway", "Norway"),
    ("Oman", "Oman"),
    ("Pakistan", "Pakistan"),
    ("Palau", "Palau"),
    ("Palestinian Territory", "Palestinian Territory"),
    ("Panama", "Panama"),
    ("Papua New Guinea", "Papua New Guinea"),
    ("Paraguay", "Paraguay"),
    ("Peru ", "Peru "),
    ("Philippines", "Philippines"),
    ("Pitcairn Islands", "Pitcairn Islands"),
    ("Poland", "Poland"),
    ("Portugal", "Portugal"),
    ("Puerto Rico", "Puerto Rico"),
    ("Qatar", "Qatar"),
    ("Reunion", "Reunion"),
    ("Romania", "Romania"),
    ("Russia", "Russia"),
    ("Rwanda", "Rwanda"),
    ("Saint Helena", "Saint Helena"),
    ("Saint Kitts and Nevis", "Saint Kitts and Nevis"),
    ("Saint Lucia", "Saint Lucia"),
    ("Saint Pierre and Miquelon", "Saint Pierre and Miquelon"),
    ("Saint Vincent and the Grenadines", "Saint Vincent and the Grenadines"),
    ("Samoa", "Samoa"),
    ("San Marino", "San Marino"),
    ("Sao Tome and Principe", "Sao Tome and Principe"),
    ("Saudi Arabia", "Saudi Arabia"),
    ("Senegal", "Senegal"),
    ("Seychelles", "Seychelles"),
    ("Sierra Leone", "Sierra Leone"),
    ("Singapore", "Singapore"),
    ("Slovakia", "Slovakia"),
    ("Slovenia", "Slovenia"),
    ("Soloman Islands", "Soloman Islands"),
    ("Somalia", "Somalia"),
    ("South Africa", "South Africa"),
    ("South Korea", "South Korea"),
    ("Spain", "Spain"),
    ("Sri Lanka", "Sri Lanka"),
    ("Sudan", "Sudan"),
    ("Suriname", "Suriname"),
    ("Swaziland", "Swaziland"),
    ("Sweden", "Sweden"),
    ("Switzerland", "Switzerland"),
    ("Syria", "Syria"),
    ("Taiwan", "Taiwan"),
    ("Tajikistan", "Tajikistan"),
    ("Tanzania", "Tanzania"),
    ("Thailand", "Thailand"),
    ("Togo", "Togo"),
    ("Tokelau", "Tokelau"),
    ("Tonga", "Tonga"),
    ("Trinidad and Tobago", "Trinidad and Tobago"),
    ("Tunisia", "Tunisia"),
    ("Turkey", "Turkey"),
    ("Turkmenistan", "Turkmenistan"),
    ("Tuvalu", "Tuvalu"),
    ("US Virgin Islands", "US Virgin Islands"),
    ("Uganda", "Uganda"),
    ("Ukraine", "Ukraine"),
    ("United Arab Emirates", "United Arab Emirates"),
    ("United Kingdom", "United Kingdom"),
    ("Uruguay", "Uruguay"),
    ("Uzbekistan", "Uzbekistan"),
    ("Vanuatu", "Vanuatu"),
    ("Vatican City", "Vatican City"),
    ("Venezuela", "Venezuela"),
    ("Vietnam", "Vietnam"),
    ("Wallis and Futuna", "Wallis and Futuna"),
    ("Western Sahara", "Western Sahara"),
    ("Yemen", "Yemen"),
    ("Yugoslavia", "Yugoslavia"),
    ("Zambia", "Zambia"),
    ("Zimbabwe", "Zimbabwe"),
    ("Other", "Other"),
)
state_choices = (("TBD", "TBD"),)
ecoregion_choices = (("TBD", "TBD"),)
habitat_choices = (
    ("Terrestrial", "Terrestrial"),
    ("Riparian", "Riparian"),
    ("Freshwater aquatic", "Freshwater aquatic"),
    ("Estuarine", "Estuarine"),
    ("Marine", "Marine"),
)
habitat_terrestrial_choices = (
    ("Forest", "Forest"),
    ("Grassland", "Grassland"),
    ("Desert", "Desert"),
    ("Heathland", "Heathland"),
    ("Agricultural", "Agricultural"),
    ("Urban/suburban", "Urban/suburban"),
    ("Tundra", "Tundra"),
)
habitat_aquatic_freshwater_choices = (
    ("Stream/river", "Stream/river"),
    ("Wetland", "Wetland"),
    ("Lake/reservoir", "Lake/reservoir"),
)
climate_choices = (
    ("Temperate", "Temperate"),
    ("Tropical/subtropical", "Tropical/subtropical"),
    ("Dry", "Dry"),
    ("Arctic/subarctic", "Arctic/subarctic"),
    ("Alpine", "Alpine"),
    ("Not specified", "Not specified"),
)
cause_term_choices = (("TBD", "TBD"),)
cause_measure_choices = (("TBD", "TBD"),)
cause_trajectory_choices = (
    ("Increase", "Increase"),
    ("Decrease", "Decrease"),
    ("Change", "Change"),
    ("Other", "Other"),
)
effect_term_choices = (("TBD", "TBD"),)
effect_measure_choices = (("TBD", "TBD"),)
effect_trajectory_choices = (
    ("Increase", "Increase"),
    ("Decrease", "Decrease"),
    ("Change", "Change"),
    ("No change", "No change"),
    ("Other", "Other"),
)
modifying_factors_choices = (("TBD", "TBD"),)
response_measure_type_choices = (
    ("Correlation coefficient", "Correlation coefficient"),
    ("R-squared", "R-squared"),
    ("Mean difference", "Mean difference"),
    ("ANOVA/PERMANOVA", "ANOVA/PERMANOVA"),
    ("Ratio", "Ratio"),
    ("Slope coefficient (beta)", "Slope coefficient (beta)"),
    ("Ordination", "Ordination"),
    ("Threshold", "Threshold"),
)
response_measure_type_correlation_choices = (
    ("Pearson", "Pearson"),
    ("Spearman", "Spearman"),
    ("Not specified", "Not specified"),
)
response_measure_type_rsq_choices = (
    ("Simple linear", "Simple linear"),
    ("Partial", "Partial"),
    ("Multiple", "Multiple"),
    ("Quantile", "Quantile"),
    ("Not specified", "Not specified"),
)
response_measure_type_ratio_choices = (
    ("Response ratio", "Response ratio"),
    ("Odds ratio", "Odds ratio"),
    ("Risk ratio", "Risk ratio"),
    ("Hazard ratio", "Hazard ratio"),
    ("Not specified", "Not specified"),
)
response_measure_type_meandiff_choices = (
    ("Non-standardized", "Non-standardized"),
    ("Standardized", "Standardized"),
    ("Not specified", "Not specified"),
)
response_measure_type_slope_choices = (
    ("Non-transformed data", "Non-transformed data"),
    ("Transformed data", "Transformed data"),
    ("Not specified", "Not specified"),
)
response_measure_type_ord_choices = (
    (
        "Canonical correspondence analysis (CCA)",
        "Canonical correspondence analysis (CCA)",
    ),
    ("Principal components analysis (PCA)", "Principal components analysis (PCA)"),
    ("Multiple discriminant analysis (MDA)", "Multiple discriminant analysis (MDA)"),
    ("Non-multidimensional scaling (NMDS)", "Non-multidimensional scaling (NMDS)"),
    ("Factor analysis", "Factor analysis"),
    ("Not specified", "Not specified"),
)
response_measure_type_thresh_choices = (
    ("Regression tree", "Regression tree"),
    ("Random forest", "Random forest"),
    ("Breakpoint (piecewise) regression", "Breakpoint (piecewise) regression"),
    ("Quantile regression", "Quantile regression"),
    ("Cumulative frequency distribution", "Cumulative frequency distribution"),
    ("Gradient forest analysis", "Gradient forest analysis"),
    ("Non-linear curve fitting", "Non-linear curve fitting"),
    ("Ordination", "Ordination"),
    ("TITAN", "TITAN"),
    ("Not specified", "Not specified"),
)
response_variability_choices = (
    ("95% CI", "95% CI"),
    ("90% CI", "90% CI"),
    ("Standard deviation", "Standard deviation"),
    ("Standard error", "Standard error"),
    ("Not applicable", "Not applicable"),
)
statistical_sig_measure_type_choices = (
    ("P-value", "P-value"),
    ("F statistic", "F statistic"),
    ("Chi square", "Chi square"),
    ("Not applicable", "Not applicable"),
)
sort_choices = (("TBD", "TBD"),)

# pick one or many field models are below


class Country(models.Model):

    country = models.CharField(
        verbose_name="Country",
        max_length=100,
        choices=country_choices,
        help_text="Select one or more countries",
    )

    def __str__(self):

        return self.country

    class Meta:
        verbose_name = "Country"


class State(models.Model):

    state = models.CharField(
        verbose_name="State",
        max_length=100,
        choices=state_choices,
        blank=True,
        help_text="Select one or more states, if applicable",
    )

    def __str__(self):

        return self.state

    class Meta:
        verbose_name = "State"


class Climate(models.Model):

    climate = models.CharField(
        verbose_name="Climate",
        max_length=100,
        choices=climate_choices,
        blank=True,
        help_text="Select one or more climates to which the evidence applies",
    )

    def __str__(self):

        return self.climate

    class Meta:
        verbose_name = "Climate"


class Ecoregion(models.Model):

    ecoregion = models.CharField(
        verbose_name="Ecoregion",
        max_length=100,
        choices=ecoregion_choices,
        blank=True,
        help_text="Select one or more Level III Ecoregions, if known",
    )

    def __str__(self):

        return self.ecoregion

    class Meta:
        verbose_name = "Ecoregion"


class Reference(models.Model):

    reference = models.CharField(max_length=100, help_text="Enter a Reference ID!")

    def __str__(self):

        return self.reference

    class Meta:
        verbose_name = "Reference"


class Metadata(models.Model):

    study_id = models.OneToOneField(Reference, on_delete=models.CASCADE)

    study_type = models.CharField(
        max_length=100, choices=study_type_choices, help_text="Select the type of study"
    )

    study_setting = models.CharField(
        max_length=100,
        choices=study_setting_choices,
        help_text="Select the setting in which evidence was generated",
    )

    country = models.ManyToManyField(Country, help_text="Select one or more countries")

    state = models.ManyToManyField(
        State, blank=True, help_text="Select one or more states, if applicable."
    )

    ecoregion = models.ManyToManyField(
        Ecoregion,
        blank=True,
        help_text="Select one or more Level III Ecoregions, if known",
    )

    habitat = models.CharField(
        verbose_name="Habitat",
        max_length=100,
        choices=habitat_choices,
        blank=True,
        help_text="Select the habitat to which the evidence applies",
    )

    habitat_terrestrial = models.CharField(
        verbose_name="Terrestrial habitat",
        max_length=100,
        choices=habitat_terrestrial_choices,
        blank=True,
        help_text="If you selected terrestrial, pick the type of terrestrial habitat",
    )

    habitat_aquatic_freshwater = models.CharField(
        verbose_name="Freshwater habitat",
        max_length=100,
        choices=habitat_aquatic_freshwater_choices,
        blank=True,
        help_text="If you selected freshwater, pick the type of freshwater habitat",
    )

    habitat_as_reported = models.TextField(
        verbose_name="Habitat as reported",
        blank=True,
        help_text="Copy and paste 1-2 sentences from article",
    )

    climate = models.ManyToManyField(
        Climate,
        blank=True,
        help_text="Select one or more climates to which the evidence applies",
    )

    climate_as_reported = models.TextField(
        verbose_name="Climate as reported",
        blank=True,
        help_text="Copy and paste from article",
    )

    def __str__(self):

        return self.study_type

    class Meta:
        verbose_name = "Metadata"


class Cause(models.Model):

    study_id = models.ForeignKey(Reference, on_delete=models.CASCADE)

    term = models.CharField(
        verbose_name="Cause term", max_length=100, choices=cause_term_choices
    )  # autocomplete

    measure = models.CharField(
        verbose_name="Cause measure", max_length=100, choices=cause_measure_choices
    )  # autocomplete

    measure_detail = models.TextField(verbose_name="Cause measure detail", blank=True)

    species = models.CharField(
        verbose_name="Cause species",
        max_length=100,
        blank=True,
        help_text="Type the species name, if applicable; use the format Common name (Latin binomial)",
    )

    units = models.CharField(
        verbose_name="Cause units",
        max_length=100,
        help_text="Type the unit associated with the cause term",
    )  # autocomplete?

    trajectory = models.CharField(
        verbose_name="Cause trajectory",
        max_length=100,
        choices=cause_trajectory_choices,
        help_text="Select qualitative description of how the cause measure changes, if applicable",
    )  # autocomplete

    comment = models.TextField(
        verbose_name="Cause comment",
        blank=True,
        help_text="Type any other useful information not captured in other fields",
    )

    as_reported = models.TextField(
        verbose_name="Cause as reported",
        help_text="Copy and paste 1-2 sentences from article",
    )

    def __str__(self):

        return self.term

    class Meta:
        verbose_name = "Cause/Treatment"


class Effect(models.Model):

    cause = models.OneToOneField(Cause, on_delete=models.CASCADE)

    term = models.CharField(
        verbose_name="Effect term", max_length=100, choices=effect_term_choices
    )

    measure = models.CharField(
        verbose_name="Effect measure", max_length=100, choices=effect_measure_choices
    )  # autocomplete

    measure_detail = models.CharField(
        verbose_name="Effect measure detail", max_length=100, blank=True
    )  # autocomplete

    species = models.CharField(
        verbose_name="Effect species",
        max_length=100,
        blank=True,
        help_text="Type the species name, if applicable; use the format Common name (Latin binomial)",
    )

    units = models.CharField(
        verbose_name="Effect units",
        max_length=100,
        help_text="Type the unit associated with the effect term",
    )  # autocomplete

    trajectory = models.CharField(
        verbose_name="Effect trajectory",
        max_length=100,
        choices=effect_trajectory_choices,
        help_text="Select qualitative description of how the effect measure changes in response to the cause trajectory, if applicable",
    )

    comment = models.TextField(
        verbose_name="Effect comment",
        blank=True,
        help_text="Type any other useful information not captured in other fields",
    )

    as_reported = models.TextField(
        verbose_name="Effect as reported",
        help_text="Copy and paste 1-2 sentences from article",
    )

    modifying_factors = models.CharField(
        verbose_name="Modifying factors",
        max_length=100,
        help_text="Type one or more factors that affect the relationship between the cause and effect",
    )  # autocomplete

    sort = models.CharField(
        verbose_name="Sort quantitative responses",
        max_length=100,
        choices=sort_choices,
        help_text="how do you want to sort multiple quantitative responses?",
        blank=True,
    )

    def __str__(self):

        return self.term

    class Meta:
        verbose_name = "Effect/Response"


class Quantitative(models.Model):

    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)

    cause_level = models.CharField(
        verbose_name="Cause treatment level",
        max_length=100,
        blank=True,
        help_text="Type the specific treatment/exposure/dose level of the cause measure",
    )

    cause_level_units = models.CharField(
        verbose_name="Cause treatment level units",
        max_length=100,
        blank=True,
        help_text="Byron added this field - does this make sense?",
    )

    cause_level_value = models.FloatField(
        verbose_name="Cause treatment level value",
        blank=True,
        help_text="Byron added this field - does this make sense?",
        null=True,
    )

    sample_size = models.IntegerField(
        verbose_name="Sample size",
        blank=True,
        help_text="Type the number of samples used to calculate the response measure value, if known",
        null=True,
    )

    measure_type_filter = models.CharField(
        verbose_name="Response measure type (filter)",
        max_length=100,
        blank=True,
        choices=response_measure_type_choices,
        help_text="This drop down will filter the following field",
    )

    measure_type = models.CharField(
        verbose_name="Response measure type",
        max_length=40,
        choices=response_measure_type_correlation_choices
        + response_measure_type_rsq_choices
        + response_measure_type_ratio_choices
        + response_measure_type_meandiff_choices
        + response_measure_type_slope_choices
        + response_measure_type_ord_choices
        + response_measure_type_thresh_choices,
        blank=True,
        help_text="Select one response measure type",
    )  # dependent on selection in response measure type column

    measure_value = models.FloatField(
        verbose_name="Response measure value",
        blank=True,
        help_text="Type the numerical value of the response measure",
        null=True,
    )

    description = models.TextField(
        verbose_name="Response measure description",
        blank=True,
        help_text="Type any other useful information not captured in other fields",
    )

    variability = models.CharField(
        verbose_name="Response variability",
        blank=True,
        max_length=100,
        choices=response_variability_choices,
        help_text="Select how variability in the response measure was reported, if applicable",
    )

    low_variability = models.FloatField(
        verbose_name="Lower response variability measure",
        blank=True,
        help_text="Type the lower numerical bound of the response variability",
        null=True,
    )

    upper_variability = models.FloatField(
        verbose_name="Upper response variability measure",
        blank=True,
        help_text="Type the upper numerical bound of the response variability",
        null=True,
    )

    statistical_sig_type = models.CharField(
        verbose_name="Statistical significance measure type",
        blank=True,
        max_length=100,
        choices=statistical_sig_measure_type_choices,
        help_text="Select the type of statistical significance measure reported",
    )

    statistical_sig_value = models.FloatField(
        verbose_name="Statistical significance measure value",
        blank=True,
        help_text="Type the numerical value of the statistical significance",
        null=True,
    )

    derived_value = models.FloatField(
        verbose_name="Derived response measure value",
        blank=True,
        help_text="Calculation from 'response measure value' based on a formula linked to 'response measure type', if applicable",
        null=True,
    )

    # def __str__(self):

    #    return self.cause_level

    class Meta:
        verbose_name = "Quantitative response information"
