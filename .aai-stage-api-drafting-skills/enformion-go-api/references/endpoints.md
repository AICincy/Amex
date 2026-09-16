# EnformionGO endpoint cache

Fetched 2026-09-13 from https://enformiongo.readme.io/llms.txt and each page's `.md` OpenAPI block.
Re-fetch those pages before changing a path or `galaxy-search-type`.

Base URL: `https://devapi.enformion.com`

Required headers on every call:

- `galaxy-ap-name`
- `galaxy-ap-password`
- `galaxy-search-type`

Plus pages list both the base type and the Plus type. Use the Plus type with the Plus path.

Where the Please Note line and the HTML header list disagree, the Please Note string is preferred and the HTML value is recorded as conflict.

## Dev APIs (single result)

| Alias | galaxy-search-type | Path | Docs |
| --- | --- | --- | --- |
| contact-enrich | DevAPIContactEnrich | /Contact/Enrich | contact-enrichment.md / contact-enrichment-search.md |
| contact-enrich-plus | DevAPIContactEnrichPlus | /Contact/EnrichPlus | contact-enrich-plus.md / search-4.md |
| caller-id | DevAPICallerID | /Phone/Enrich | caller-id.md / caller-id-search.md |
| caller-id-plus | DevAPICallerIDPlus | /Phone/EnrichPlus | caller-id-plus.md / search-6.md |
| email-id | DevAPIEmailID | /Email/Enrich | email-id.md / email-id-search.md |
| email-id-plus | DevAPIEmailIDPlus | /Email/EnrichPlus | email-id-enrich-plus.md / search-7.md |
| contact-id | DevAPIContactID | /Contact/Id | contact-id.md / contact-id-search.md |
| contact-id-plus | DevAPIContactIDPlus | /Contact/IdPlus | contact-id-plus.md / search-5.md |
| address-id | DevAPIAddressID | /Address/Id | address-id.md / address-id-search.md |
| address-id-plus | DevAPIAddressIDPlus | /Address/IdPlus | address-id-plus.md / search-8.md |
| address-autocomplete | DevAPIAddressAutoComplete | /Address/AutoComplete | address-autocomplete.md / address-autocomplete-search.md |

## People and verify

| Alias | galaxy-search-type | Path | Docs |
| --- | --- | --- | --- |
| elead-verify | LeadVerify | /eIDV/eLeadVerify | eleadverify.md / search-3.md |
| person-search | Person | /PersonSearch | person-search.md / search.md |
| person-teaser | Teaser | /PersonSearch | person-search.md |
| reverse-phone-person-teaser | ReversePhonePersonTeaser | /PersonSearch | person-search.md |
| reverse-phone-person | ReversePhonePerson | /PersonSearch | person-search.md |
| id-verification | DevAPIIDVerification | /Identity/Verify_Id | id-verification.md / id-verification-search.md |
| census-search | Census | /CensusSearch | census.md / census-search.md |
| debt-v2 | DebtV2 | /DebtSearch/V2 | debt-v2.md / debt-v2-search.md |
| divorce-search | Divorce | /DivorceSearch | divorce.md / divorce-search.md |
| marriage-search | Marriage | /MarriageSearch | marriage.md / marriage-search.md |
| reverse-phone | ReversePhone | /ReversePhoneSearch | reverse-phone.md / reverse-phone-search.md |
| linkedin-id | LinkedinID | /LinkedIn/Id | linkedin-id.md / search-1.md |

ELeadVerify conflict: Please Note `LeadVerify`, HTML list `IdvAuthPerson`.
Linkedin ID conflict: Please Note `LinkedinID`, HTML list `ReversePhone`.

## Business and property

| Alias | galaxy-search-type | Path | Docs |
| --- | --- | --- | --- |
| business-search | BusinessV2 | /BusinessV2Search | business.md / business-search.md |
| domain-search | Domain | /DomainSearch | domain.md / domain-search.md |
| workplace-search | Workplace | /WorkplaceSearch | workplace.md / workplace-search.md |
| business-id | BusinessID | /Business/Id | business-id.md / search-2.md |
| property-v2 | PropertyV2 | /PropertyV2Search | property-v2.md / property-v2-search.md |

Business ID conflict: Please Note `BusinessID`, HTML list `BusinessV2`.

## Court and asset (PRO)

| Alias | galaxy-search-type | Path | Docs |
| --- | --- | --- | --- |
| criminal-v2 | CriminalV2 | /CriminalSearch/V2 | criminal-search-v2.md / criminal-search-v2-search.md |
| eviction | Eviction | /EvictionSearch | eviction.md / eviction-search.md |
| pre-foreclosure | ForeclosureV2 | /ForeclosureV2Search | pre-foreclosure.md / pre-foreclosure-search.md |
| ofac | Ofac | /OfacSearch | ofac.md / ofac-search.md |
| vehicle-ownership | VehicleRegistrationSearch | /VehicleRegistrationSearch | vehicle-ownership.md / vehicle-ownership-search.md |
| dea | Dea | /deasearch | dea.md / dea-search.md |
| professional-license | ProLicense | /ProLicenseSearch | professional-license.md / professional-license-search.md |

DEA type confirmed as `Dea` on dea.md.

## Data alerts

| Alias | galaxy-search-type | Path | Docs |
| --- | --- | --- | --- |
| alerts-add | DataAlertsAddSubscription | /DataAlerts/AddSubscription | add-subscription.md |
| alerts-get | DataAlertsGetSubscription | /DataAlerts/GetSubscription | get-subscription.md |
| alerts-remove | DataAlertsRemoveSubscription | /DataAlerts/RemoveSubscription | remove-subscription.md |
| alerts-get-alert | DataAlertsGetAlert | /DataAlerts/GetAlert | get-alert.md |
| alerts-count | DataAlertsCountAlert | /DataAlerts/CountAlert | count-alert.md |

Confirm Get/Count search-type strings on those pages if a call fails.

## Workplace drilldown

Endpoint path only. Confirm method and search-type on the live page before calling.

| Alias | Path |
| --- | --- |
| workplace-states | /WorkplaceSearch/GetStates |
| workplace-cities | /WorkplaceSearch/GetCities |
| workplace-industries | /WorkplaceSearch/GetIndustries |
| workplace-levels | /WorkplaceSearch/GetLevels |
| workplace-departments | /WorkplaceSearch/GetDepartments |
| workplace-job-titles | /WorkplaceSearch/GetJobTitles |

Regional variants exist on the Get * (Regional) pages.

## Source files this run

Store any user-authorized working copy in the current task workspace. Do not
embed a host-specific artifact path in this package.
