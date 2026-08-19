# Power Query M Scripts

Each block below creates one Power Query table from one CSV. Create one Blank Query per block, rename the query to the heading, and paste the block into Advanced Editor.

Do not combine these scripts into one query.

## page1_canadian_donor_overall

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page1_canadian_donor_overall.csv"),
        [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"metric", type text},
        {#"sample_value", type text},
        {#"weighted_value", type text},
        {#"sample_value_numeric", type number},
        {#"weighted_value_numeric", type number},
        {#"value_type", type text},
        {#"note", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## page1_canadian_donor_segments

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page1_canadian_donor_segments.csv"),
        [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"segment_variable", type text},
        {#"segment", type text},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"sample_donor_rate_pct", type number},
        {#"weighted_donor_rate_pct", type number},
        {#"donor_sample_n", Int64.Type},
        {#"weighted_donors", type number},
        {#"weighted_mean_donation", type number},
        {#"weighted_median_donation", type number},
        {#"weighted_mean_frequency", type number},
        {#"weighted_median_frequency", type number},
        {#"sort_order", Int64.Type}
        },
        "en-US"
    )
in
    ChangedType
```

## page1_donation_amount_bands

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page1_donation_amount_bands.csv"),
        [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"amount_band", type text},
        {#"donor_sample_n", Int64.Type},
        {#"weighted_donors", type number},
        {#"weighted_donor_share_pct", type number},
        {#"weighted_total_donations", type number},
        {#"weighted_dollar_share_pct", type number},
        {#"sort_order", Int64.Type}
        },
        "en-US"
    )
in
    ChangedType
```

## page1_donation_frequency

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page1_donation_frequency.csv"),
        [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"donation_count", Int64.Type},
        {#"donor_sample_n", Int64.Type},
        {#"weighted_donors", type number},
        {#"weighted_donor_share_pct", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_donation_distribution

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_donation_distribution.csv"),
        [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"amount_band", type text},
        {#"sort_order", Int64.Type},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"weighted_health_donor_share_pct", type number},
        {#"weighted_health_donation_dollars", type number},
        {#"weighted_health_dollar_share_pct", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_donor_group_comparison

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_donor_group_comparison.csv"),
        [Delimiter=",", Columns=19, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"group", type text},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"sample_charitable_donor_n", Int64.Type},
        {#"weighted_charitable_donors", type number},
        {#"weighted_charitable_donor_rate_pct", type number},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"weighted_health_donor_rate_population_pct", type number},
        {#"weighted_health_donor_rate_among_donors_pct", type number},
        {#"weighted_mean_total_donation_among_group_donors", type text},
        {#"weighted_median_total_donation_among_group_donors", type text},
        {#"weighted_mean_total_frequency_among_group_donors", type text},
        {#"weighted_median_total_frequency_among_group_donors", type text},
        {#"weighted_total_health_dollars", type number},
        {#"weighted_mean_health_donation", type number},
        {#"weighted_median_health_donation", type number},
        {#"weighted_mean_health_frequency", type number},
        {#"weighted_median_health_frequency", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_donor_overview

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_donor_overview.csv"),
        [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"metric", type text},
        {#"sample_value", type text},
        {#"weighted_value", type text},
        {#"sample_value_numeric", type number},
        {#"weighted_value_numeric", type number},
        {#"value_type", type text},
        {#"note", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_donor_volunteering

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_donor_volunteering.csv"),
        [Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"comparison_group", type text},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"sample_volunteer_n", Int64.Type},
        {#"weighted_volunteers", type number},
        {#"weighted_volunteering_valid_denominator", type number},
        {#"weighted_volunteer_rate_pct", type number},
        {#"sample_fundraising_volunteer_n", Int64.Type},
        {#"weighted_fundraising_volunteers", type number},
        {#"weighted_fundraising_valid_denominator", type number},
        {#"weighted_fundraising_volunteer_rate_pct", type number},
        {#"sample_healthcare_support_volunteer_n", Int64.Type},
        {#"weighted_healthcare_support_volunteers", type number},
        {#"weighted_healthcare_support_valid_denominator", type number},
        {#"weighted_healthcare_support_volunteer_rate_pct", type number},
        {#"volunteer_sample_n_with_hours", Int64.Type},
        {#"weighted_mean_volunteer_hours_among_volunteers", type number},
        {#"weighted_median_volunteer_hours_among_volunteers", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_profile_age

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_profile_age.csv"),
        [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"segment_variable", type text},
        {#"segment_code", Int64.Type},
        {#"segment_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"sample_charitable_donor_n", Int64.Type},
        {#"weighted_charitable_donors", type number},
        {#"weighted_charitable_donor_rate_pct", type number},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"weighted_health_donor_rate_population_pct", type number},
        {#"weighted_health_donor_rate_among_donors_pct", type number},
        {#"weighted_health_donor_composition_pct", type number},
        {#"weighted_mean_health_donation", type number},
        {#"weighted_median_health_donation", type number},
        {#"weighted_mean_total_giving_health_donors", type number},
        {#"weighted_median_total_giving_health_donors", type number},
        {#"weighted_mean_total_giving_nonhealth_donors", type number},
        {#"weighted_median_total_giving_nonhealth_donors", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_profile_education

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_profile_education.csv"),
        [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"segment_variable", type text},
        {#"segment_code", Int64.Type},
        {#"segment_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"sample_charitable_donor_n", Int64.Type},
        {#"weighted_charitable_donors", type number},
        {#"weighted_charitable_donor_rate_pct", type number},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"weighted_health_donor_rate_population_pct", type number},
        {#"weighted_health_donor_rate_among_donors_pct", type number},
        {#"weighted_health_donor_composition_pct", type number},
        {#"weighted_mean_health_donation", type number},
        {#"weighted_median_health_donation", type number},
        {#"weighted_mean_total_giving_health_donors", type number},
        {#"weighted_median_total_giving_health_donors", type number},
        {#"weighted_mean_total_giving_nonhealth_donors", type number},
        {#"weighted_median_total_giving_nonhealth_donors", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_profile_income

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_profile_income.csv"),
        [Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"segment_variable", type text},
        {#"segment_code", Int64.Type},
        {#"segment_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"sample_charitable_donor_n", Int64.Type},
        {#"weighted_charitable_donors", type number},
        {#"weighted_charitable_donor_rate_pct", type number},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"weighted_health_donor_rate_population_pct", type number},
        {#"weighted_health_donor_rate_among_donors_pct", type number},
        {#"weighted_health_donor_composition_pct", type number},
        {#"weighted_mean_health_donation", type number},
        {#"weighted_median_health_donation", type number},
        {#"weighted_mean_total_giving_health_donors", type number},
        {#"weighted_median_total_giving_health_donors", type number},
        {#"weighted_mean_total_giving_nonhealth_donors", type number},
        {#"weighted_median_total_giving_nonhealth_donors", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page2_health_profile_province

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page2_health_profile_province.csv"),
        [Delimiter=",", Columns=21, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"segment_variable", type text},
        {#"segment_code", Int64.Type},
        {#"segment_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"sample_charitable_donor_n", Int64.Type},
        {#"weighted_charitable_donors", type number},
        {#"weighted_charitable_donor_rate_pct", type number},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"weighted_health_donor_rate_population_pct", type number},
        {#"weighted_health_donor_rate_among_donors_pct", type number},
        {#"weighted_health_donor_composition_pct", type number},
        {#"weighted_mean_health_donation", type number},
        {#"weighted_median_health_donation", type number},
        {#"weighted_mean_total_giving_health_donors", type number},
        {#"weighted_median_total_giving_health_donors", type number},
        {#"weighted_mean_total_giving_nonhealth_donors", type number},
        {#"weighted_median_total_giving_nonhealth_donors", type number},
        {#"reliability_note", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## page3_channel_by_health_value

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page3_channel_by_health_value.csv"),
        [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"segment_variable", type text},
        {#"segment_label", type text},
        {#"channel_key", type text},
        {#"channel_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"valid_denominator_weighted", type number},
        {#"sample_channel_user_n", Int64.Type},
        {#"weighted_channel_users", type number},
        {#"weighted_channel_use_rate_pct", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page3_giving_behaviour_summary

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page3_giving_behaviour_summary.csv"),
        [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"comparison_group", type text},
        {#"behaviour_variable", type text},
        {#"behaviour_label", type text},
        {#"response_code", Int64.Type},
        {#"response_label", type text},
        {#"sample_n", Int64.Type},
        {#"weighted_population", type number},
        {#"weighted_response_pct", type number},
        {#"valid_denominator_weighted", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page3_giving_channel_summary

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page3_giving_channel_summary.csv"),
        [Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"comparison_group", type text},
        {#"channel_key", type text},
        {#"channel_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_donor_n", Int64.Type},
        {#"weighted_donors", type number},
        {#"valid_channel_denominator_weighted", type number},
        {#"sample_channel_user_n", Int64.Type},
        {#"weighted_channel_users", type number},
        {#"weighted_channel_use_rate_pct", type number},
        {#"weighted_channel_donation_dollars", type number},
        {#"weighted_mean_channel_donation_among_users", type number},
        {#"weighted_median_channel_donation_among_users", type number},
        {#"weighted_mean_channel_frequency_among_users", type number},
        {#"weighted_median_channel_frequency_among_users", type number},
        {#"health_vs_nonhealth_rate_gap_pct_points", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page4_motivation_by_age

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page4_motivation_by_age.csv"),
        [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"segment_variable", type text},
        {#"segment_label", type text},
        {#"motivation_variable", type text},
        {#"motivation_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"valid_denominator_weighted", type number},
        {#"sample_yes_n", Int64.Type},
        {#"weighted_yes", type number},
        {#"weighted_yes_pct", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page4_motivation_by_health_value

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page4_motivation_by_health_value.csv"),
        [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"segment_variable", type text},
        {#"segment_label", type text},
        {#"motivation_variable", type text},
        {#"motivation_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"valid_denominator_weighted", type number},
        {#"sample_yes_n", Int64.Type},
        {#"weighted_yes", type number},
        {#"weighted_yes_pct", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page4_motivation_summary

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page4_motivation_summary.csv"),
        [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"comparison_group", type text},
        {#"motivation_variable", type text},
        {#"motivation_label", type text},
        {#"sort_order", Int64.Type},
        {#"sample_donor_n", Int64.Type},
        {#"weighted_donors", type number},
        {#"valid_denominator_weighted", type number},
        {#"sample_yes_n", Int64.Type},
        {#"weighted_yes", type number},
        {#"weighted_yes_pct", type number},
        {#"health_vs_nonhealth_gap_pct_points", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page5_barrier_category_summary

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page5_barrier_category_summary.csv"),
        [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"comparison_group", type text},
        {#"barrier_category", type text},
        {#"mean_weighted_yes_pct", type number},
        {#"max_weighted_yes_pct", type number},
        {#"strongest_barrier", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## page5_barrier_summary

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page5_barrier_summary.csv"),
        [Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"comparison_group", type text},
        {#"barrier_variable", type text},
        {#"barrier_label", type text},
        {#"barrier_category", type text},
        {#"applicability", type text},
        {#"sort_order", Int64.Type},
        {#"sample_group_n", type text},
        {#"weighted_group_population", type text},
        {#"valid_denominator_weighted", type number},
        {#"sample_yes_n", Int64.Type},
        {#"weighted_yes", type number},
        {#"weighted_yes_pct", type number},
        {#"health_vs_nonhealth_gap_pct_points", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page5_barriers_by_income

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page5_barriers_by_income.csv"),
        [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"chapter", type text},
        {#"segment_variable", type text},
        {#"segment_label", type text},
        {#"barrier_variable", type text},
        {#"barrier_label", type text},
        {#"barrier_category", type text},
        {#"sort_order", Int64.Type},
        {#"sample_health_donor_n", Int64.Type},
        {#"weighted_health_donors", type number},
        {#"valid_denominator_weighted", type number},
        {#"sample_yes_n", Int64.Type},
        {#"weighted_yes", type number},
        {#"weighted_yes_pct", type number}
        },
        "en-US"
    )
in
    ChangedType
```

## page6_evidence_table

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page6_evidence_table.csv"),
        [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"evidence_theme", type text},
        {#"source_chapter", type text},
        {#"metric", type text},
        {#"value", type text},
        {#"interpretation", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## page6_priority_audiences

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page6_priority_audiences.csv"),
        [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"priority_rank", Int64.Type},
        {#"audience_name", type text},
        {#"opportunity_type", type text},
        {#"who_they_are", type text},
        {#"what_the_data_shows", type text},
        {#"why_they_matter", type text},
        {#"how_they_currently_give", type text},
        {#"what_appears_to_motivate_them", type text},
        {#"what_barriers_may_matter", type text},
        {#"fundraising_approach_supported", type text},
        {#"what_data_does_not_allow_us_to_claim", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## page7_bonus_model_metrics

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page7_bonus_model_metrics.csv"),
        [Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"threshold", type number},
        {#"roc_auc", type number},
        {#"precision", type number},
        {#"recall", type number},
        {#"f1", type number},
        {#"true_positive", Int64.Type},
        {#"false_positive", Int64.Type},
        {#"true_negative", Int64.Type},
        {#"false_negative", Int64.Type},
        {#"test_sample_n", Int64.Type},
        {#"train_sample_n", Int64.Type},
        {#"test_health_donor_rate", type number},
        {#"train_health_donor_rate", type number},
        {#"model", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## page7_bonus_top_model_coefficients

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\page7_bonus_top_model_coefficients.csv"),
        [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"feature", type text},
        {#"coefficient", type number},
        {#"odds_ratio_per_standardized_unit", type number},
        {#"direction", type text}
        },
        "en-US"
    )
in
    ChangedType
```

## powerbi_data_manifest

```powerquery
let
    Source = Csv.Document(
        File.Contents("outputs\\powerbi\\powerbi_data_manifest.csv"),
        [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedType = Table.TransformColumnTypes(
        PromotedHeaders,
        {
        {#"powerbi_file", type text},
        {#"source_file", type text},
        {#"dashboard_page", type text},
        {#"table_grain", type text},
        {#"rows", Int64.Type},
        {#"columns", Int64.Type},
        {#"sha256", type text}
        },
        "en-US"
    )
in
    ChangedType
```
