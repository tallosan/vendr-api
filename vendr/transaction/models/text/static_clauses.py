# -*- coding: utf-8 -*-
#
# Static Clauses.
#
# We'll represent each clause as a dictionary with a set of keys:
#
# Clause title, explanation, preview, & required (whether or not the clause is a
# notice of fulfillment requirement).
#
# ===============================================================================


BLANK_FIELD = '__'

# Completion Date Adjustment clause.
completion_date_adjustments_title = 'Completion Date Adjustments'
completion_date_adjustments_pre = 'Notwithstanding the completion date set out in ' + \
        'the Agreement, the parties in this Agreement may, by mutual agreement ' + \
        'in writing, advance or extend the completion date of this transaction. '
completion_date_adjustments = {
        'title': completion_date_adjustments_title,
        'preview': completion_date_adjustments_pre,
        'explanation': 'Any changes to the completion date must be agreed, in writing, by the Buyer and the Seller. This is to ensure changes aren’t made to benefit only one party, and both parties are satisfied with the change.',
        'required': False
}

buyer_negligence_title = 'Buyer Negligence'
buyer_negligence_pre = "The parties hereto consent and agree that should this transaction not be completed, solely due to the Buyer's default or neglect, the deposit funds held by the Deposit Holder shall be released to the Seller forthwith, on the date following the date of completion set out in this Agreement, provided all proper legal protocols are followed."
buyer_negligence = {
        'title': buyer_negligence_title,
        'preview': buyer_negligence_pre,
        'explanation': 'If the transaction fails simply because the Buyer defaults or neglects this transaction, the Seller is allowed to take the proper legal protocols to remedy any damages.',
        'required': False
}

# Chattels and Fixtures clause.
chattels_and_fixtures_pre = 'The Seller represents and warrants that the ' + \
        'chattels and fixtures as included in this Agreement will be in good ' + \
        'working order and free from liens and encumbrances on completion. The ' + \
        'parties in this Agreement of Purchase and Sale agree that this ' + \
        'representation and warranty shall survive and not merge on completion ' + \
        'of this transaction, but apply only to those circumstances existing at ' + \
        'the date of completion stated herein.'
chattels_and_fixtures_gen = 'Chattels and Fixtures Clause'
chattels_and_fixtures = {
        'preview': chattels_and_fixtures_pre,
        'generator': chattels_and_fixtures_gen,
        'explanation': 'All the Chattels (moveable possessions, such as fridges) and Fixtures (immovable possessions, such as water heaters) listed in this agreement, must be in good working order by the completion date. There should also be no legal claim(s) against any of the specified possessions in this Agreement.',
        'required': True
}

re_inspect_pre = 'The Buyer shall have the right to inspect the property one further time prior to completion, at a mutually agreed upon time, provided that notice is given to the Seller. The Seller agrees to provide access to the property for purpose of this inspection. In the event the foregoing condition is not fulfilled or waived by the Buyer, if procured, the Buyer agrees to provide the Seller with a true copy of the Inspection Report and all estimates related thereto prior to the return of the deposit herein.'
re_inspect_gen = 'Re-Inspection Clause'
re_inspect = {
        'preview': re_inspect_pre,
        'generator': re_inspect_gen,
        'explanation': 'The Buyer shall have the right to inspect the property one further time prior to completion, at a mutually agreed upon time, provided that notice is given to the Seller. The Seller agrees to provide access to the property for purpose of this inspection. In the event the foregoing condition is not fulfilled or waived by the Buyer, if procured, the Buyer agrees to provide the Seller with a true copy of the Inspection Report and all estimates related thereto prior to the return of the deposit herein.',
        'required': True
}

title_search_title = 'Title Search'
title_search_pre = 'Seller hereby consents to the Landlord of the Land, the municipality or other governmental agencies releasing to Buyer details of all outstanding work orders, deficiency notices and all matters affecting the property, and Seller agrees to execute and deliver such further authorizations in this regard as Buyer may reasonably require. Buyer shall be allowed until the Completion Date (Requisition Date), to examine the title to the Property at the Buyer’s own expense, to satisfy Buyer that there are no outstanding work orders, deficiency notices or other matters affecting the Property, and that its present use may be lawfully continued and that the principal building may be insured against risk of fire.'
title_search = {
        'title': title_search_title,
        'preview': title_search_pre,
        'generator': 'The Seller will grant the Buyer access to all title information concerning the property. The Seller will provide any government documents to the Buyer upon request, such as work orders. Seller must fix any issues that arise from this search, or this agreement is canceled.',
        'explanation': 'The Seller will grant the Buyer access to all title information concerning the property. The Seller will provide any government documents to the Buyer upon request, such as work orders. Seller must fix any issues that arise from this search, or this agreement is canceled.',
        'required': True
}

title_title = 'Title'
title_pre = 'Buyer agrees to accept title to the Property subject to all rights and easements registered against title for the supply and installation of telephone services, electricity, gas, sewers, water, television cable facilities and other related services; provided that the title to the property is otherwise good and free from all registered restrictions, charges, liens, and encumbrances except: (a) as herein expressly provided; (b) any registered restrictions, conditions or covenants that run with the land providing that such are complied with; (c)  any registered municipal agreements and registered agreements with publicly regulated utilities providing such have been complied with, or security has been posted to ensure compliance and completion, as evidenced by a letter from the relevant municipality or regulated utility; (d) the provisions of the Condominium Act and its Regulations and the terms, conditions and provisions of the Declaration, Description and By-laws, Occupancy Standards By-laws, including the Common Element Rules and other Rules and Regulations; (e) any minor easements for the supply of domestic utility or telephone services to the property or adjacent properties; (f) any easements for drainage, storm or sanitary sewers, public utility lines, telephone lines, cable television lines or other services which do not materially affect the use of the property; and (g) any existing municipal agreements, zoning by-laws and/or regulations and utilities or service contracts. If by the Completion Date (Requisition Date) any valid objection to title or to any outstanding work order or deficiency notice, or to the fact the said present use may not lawfully be continued, or that the principal building may not be insured against risk of fire is made in writing to Seller and which Seller is unable or unwilling to remove, remedy or satisfy or obtain insurance save and except against risk of fire (Title Insurance) in favour of the Buyer and any mortgagee, (with all related costs at the expense of the Seller), and which Buyer will not waive, this Agreement notwithstanding any intermediate acts or negotiations in respect of such objections, shall be at an end and all monies paid shall be returned without interest or deduction. Save as to any valid objection so made by such day and except for any objection going to the root of the title, Buyer shall be conclusively deemed to have accepted Seller’s title to the property.'
title = {
        'title': title_title,
        'preview': title_pre,
        'explanation': 'After assessing the title to the property, the Buyer agrees to accept the title to the property subject to any applicable laws and rules on the usage of the property and municipal services (e.g. zoning bylaws, condominium corporation’s declaration, municipal agreements, etc.).',
        'required': True
}

future_use_pre = 'Seller and Buyer agree that there is no representation or warranty of any kind that the future intended use of the property by Buyer is or will be lawful except as may be specifically provided for in this Agreement.'
future_use_gen = 'Future Use Clause'
future_use = {
        'preview': future_use_pre,
        'generator': future_use_gen,
        'explanation': 'hi',
        'required': False
}

documents_request_title = 'Documents Request'
documents_request_pre = 'A request for the preparation or production of any title deed, abstract, survey or other evidence of title to the property by the Buyer, shall not be called for except such as are in the possession or control of the Seller. At the request of the Buyer, the Seller will deliver any sketch or survey of the property within Seller’s control to Buyer immediately and prior to the Requisition Date.'
documents_request = {
        'title': documents_request_title,
        'preview': documents_request_pre,
        'explanation': 'The Seller must provide the Buyer with any information concerning the property that is evidence of title. The Seller will provide such information to the Buyer upon request immediately and prior to the completion date (e.g. survey and deed).',
        'required': True
}

discharge_title = 'Discharge'
discharge_pre = 'If a discharge of any Charge/Mortgage held by a corporation incorporated pursuant to the Trust And Loan Companies Act (Canada), Chartered Bank, Trust Company, Credit Union, Caisse Populaire or Insurance Company and which is not to be assumed by the Buyer on completion, is unavailable in registrable form on completion, Buyer agrees to accept Seller’s lawyer’s personal undertaking to obtain, out of the closing funds, a discharge in registrable form and to register same, or cause same to be registered, on title within a reasonable period of time after completion, provided that on or before completion Seller shall provide to Buyer a mortgage statement prepared by the mortgagee, lienholder or encumbrancer  setting out the balance required to obtain the discharge, and, where a real-time electronic cleared funds transfer system is not being used, a direction executed by Seller directing payment to the mortgagee, lienholder or encumbrancer  of the amount required to obtain the discharge out of the balance due on completion.'
discharge = {
        'title': discharge_title,
        'preview': discharge_pre,
        'explanation': 'If the Seller has a mortgage with a chartered bank, trust company, insurance company, credit union or Caisse Populaire, it will most likely not be discharged on or before the completion date. In this case the Buyer will receive from the Seller a mortgage statement disclosing the discharge amount and the discharge date. All other mortgages will have to be discharged by the completion date.',
        'required': False
}

inspection_omit_title = 'Omit Inspection'
inspection_omit_pre = 'The Buyer understands that upon acceptance of this offer there shall be a binding agreement of purchase and sale between Buyer and Seller. The Buyer acknowledges having the opportunity to include a requirement for a property inspection report in this Agreement and agrees that except as may be specifically provided for in this Agreement of purchase and sale, the Buyer will not be obtaining a property inspection or property inspection report regarding the Property. Buyer acknowledges having had the opportunity to inspect the said Property.'
inspection_omit = {
        'title': inspection_omit_title,
        'preview': inspection_omit_pre,
        'explanation': 'The Buyer acknowledges that they had the opportunity to inspect the property, by utilizing the services of a professional inspector. The Buyer also acknowledges the importance of a property inspection and still chooses not to have one performed on the property.',
        'required': False
}

insurance_title = 'Insurance'
insurance_pre = 'All buildings and all other things being purchased on the property shall be and remain until completion at the risk of Seller. Pending completion, all insurance policies, if any, shall be held by the Seller and the proceeds thereof in trust for the parties as their interests may appear and in the event of substantial damage, either this offer shall be null and void and all the monies paid returned without interest or deduction or else the Buyer take the proceeds of any insurance and complete the purchase. No insurance shall be transferred on completion. Buyer shall supply Seller with reasonable evidence of adequate insurance if Seller is taking back a Charge/ Mortgage, or Buyer is assuming a Charge/Mortgage, in order to protect Seller’s or other mortgagee’s interest on the date of completion.'
insurance = {
        'title': insurance_title,
        'preview': insurance_pre,
        'explanation': 'The Seller is responsible for the property until closing and must maintain insurance on the property until the completion date. In the event of substantial damage to the property, the Buyer can cancel the Agreement, or can complete this transaction and get the proceeds of any insurance.',
        'required': True
}

planning_title = 'Planning'
planning_pre = 'This Agreement shall be effective to create an interest in the property only if Seller complies with the subdivision control provisions of the Planning Act by completion and Seller covenants to proceed diligently at Seller’s expense to obtain any necessary consent by completion.'
planning = {
        'title': planning_title,
        'preview': planning_pre,
        'explanation': 'The Seller will comply with any and all Planning bylaws in the Planning Act concerning the property. The Seller will ensure that they have obtained the approval needed to sell the property.',
        'required': True
}

document_prep_title = 'Document Preparation'
document_prep_pre = 'This Agreement shall be effective to create an interest in the property only if Seller complies with the subdivision control provisions of the Planning Act by completion and Seller covenants to proceed diligently at Seller’s expense to obtain any necessary consent by completion.'
document_prep = {
        'title': document_prep_title,
        'preview': document_prep_pre,
        'explanation': 'The deed/ transfer will be registered at the Seller’s expense (except the land transfer tax affidavit) and any mortgage given to the Buyer is at the Buyer’s expense.',
        'required': False
}

residency_title = 'Residency'
residency_pre = 'Provided that is the Seller is not a non-resident under the non-residency provisions of the Income Tax Act, the Seller represents and warrants that the Seller is not and on completion will not be a non-resident under the non-residency provisions of the Income Tax Act which representation and warranty shall survive and not merge upon the date of completion and the Seller shall deliver to the Buyer a statutory declaration that Seller is not then a non-resident of Canada'
residency = {
        'title': residency_title,
        'preview': residency_pre,
        'explanation': 'Non-residents must pay different taxes than residences, as such residency must be disclosed during this transaction.',
        'required': False
}

non_residency_title = 'Non-Residency'
non_residency_pre = 'Provided that if the Seller is a non-resident under the non-residency provisions of the Income Tax Act, the Buyer shall be credited towards the Purchase Price with the amount, if any, necessary for Buyer to pay to the Minister of National Revenue to satisfy Buyer’s liability in respect of tax payable by Seller under the non-residency provisions of the Income Tax Act by reason of this sale. Buyer shall not claim such credit if Seller delivers on completion the prescribed certificate.'
non_residency = {
        'title': non_residency_title,
        'preview': non_residency_pre,
        'explanation': 'Non-residents must pay different taxes than residences, as such residency must be disclosed during this transaction.',
        'required': False
}

adjustments_title = 'Adjustments'
adjustments_pre = 'The Buyer shall assume any rents, mortgage interest, taxes,  local improvement rates/assessments  and unmetered public or private utility charges and unmetered cost of fuel, as applicable, from, and including, the date set for completion and shall be apportioned to the Buyer and allowed to the date of completion.'
adjustments = {
        'title': adjustments_title,
        'preview': adjustments_pre,
        'explanation': 'All additional property expenses, such as rent, mortgage interest, taxes, and utility payments, on the completion date and after the completion date, will be applicable to the Buyer and will be paid by the Buyer. All expenses before the completion date, will be paid by the Seller.',
        'required': False
}

deadline_extensions_title = 'Time Limits'
deadline_extensions_pre = 'Time shall in all respects be of the essence hereof provided that the time for doing or completing of any matter provided for herein may be extended or abridged by an agreement in writing signed by Seller and Buyer or by their respective lawyers who may be specifically authorized in that regard.'
deadline_extensions = {
        'title': deadline_extensions_title,
        'preview': deadline_extensions_pre,
        'explanation': 'Dates and time in this transaction are of extreme importance and must be followed.',
        'required': False
}

tender_title = 'Tender'
tender_pre = 'Any tender of documents or money hereunder may be made upon Seller or Buyer or their respective lawyers on the date set for completion. Using the Large Value Transfer System, consideration shall be tendered with funds drawn on a lawyer’s trust account in the form of a bank draft, certified cheque or wire transfer.'
tender = {
        'title': tender_title,
        'preview': tender_pre,
        'explanation': 'Buyers must be able to produce the money to complete the transaction, and Seller must be able to provide the property information required to close this transaction.',
        'required': False
}

family_law_title = 'Family Law Act'
family_law_pre = 'Under the provisions of the Family Law Act, R.S.O.1990 the Seller warrants that spousal consent is not necessary to this transaction unless Seller’s spouse has executed the consent hereinafter provided.'
family_law = {
        'title': family_law_title,
        'preview': family_law_pre,
        'explanation': 'The Seller warrants that they have complied with the Family law Act as it relates to this transaction and that no spouse has a claim to the property other than a spouse who has signed a consent in the area set in this agreement.',
        'required': False
}

toxic_substance_pre = 'Seller represents and warrants to Buyer that during the time Seller has owned the property, the Seller has not caused any building on the property to be insulated with insulation containing urea formaldehyde, vermiculite and/or any other hazardous substance which materially affects the use of the property, and that to the best of Seller’s knowledge no building on the property contains or has ever contained insulation that contains urea formaldehyde, vermiculite and/or other hazardous substance, which materially affects the use of the property. This warranty shall survive and not merge on the date of completion, and if the building is part of a multiple unit building, this warranty shall only apply to that part of the building which is the subject of this transaction.'
toxic_substance_gen = 'UFFI and Vermiculite Clause'
toxic_substance = {
        'preview': toxic_substance_pre,
        'generator': toxic_substance_gen,
        'explanation': 'this one is empty for some reason!',
        'required': False
}

agreement_in_writing_title = 'Agreement In Writing'
agreement_in_writing_pre = 'For the purposes of this Agreement, Seller means vendor and Buyer means purchaser. This Agreement including any Additional Terms attached hereto, shall constitute the entire Agreement between Buyer and Seller. If there is conflict or discrepancy between any provision added to this Agreement (including any Additional Terms attached hereto) and any provision in the standard pre-set portion hereof, the added provision shall supersede the standard pre-set provision to the extent of such conflict or discrepancy. There is no representation, warranty, collateral agreement or condition, which affects this Agreement other than as expressed herein. This Agreement shall be read with all changes of gender or number required by the context.'
agreement_in_writing = {
        'title': agreement_in_writing_title,
        'preview': agreement_in_writing_pre,
        'explanation': 'If there is a conflict or discrepancy between any of the pre-set clauses and anything that has been added to the agreement, then added parts supersede the pre-set clauses.',
        'required': False
}

time_and_date_title = 'Time and Date'
time_and_date_pre = 'Any reference to a time and date in this Agreement shall mean the time and date where the said property is located.'
time_and_date = {
        'title': time_and_date_title,
        'preview': time_and_date_pre,
        'explanation': 'Time and date in this agreement are determined by the location of the property in this agreement.',
        'required': False
}

electronic_title = 'Electronic'
electronic_pre = 'As amended with respected to this Agreement and any other documents respecting this transaction the Buyer and Seller hereto consent and agree to the use of electronic signature pursuant to the Electronic Commerce Act 2000, S.O. 2000, c17.'
electronic = {
        'title': electronic_title,
        'preview': electronic_pre,
        'explanation': 'Electronic signatures on this document are binding under Canadian law.',
        'required': False
}

property_tax_assess_title = 'Property Tax Assessment'
property_tax_assess_pre = ' The parties hereto agree that no claim will be made against the Buyer or Seller, for any changes in property tax as a result of a re-assessment of the said property, save and except any property taxes that accrued pending  the completion of this transaction. The parties to this Agreement hereby acknowledge that the Province of Ontario has implemented current value assessment and properties may be re-assessed on an annual basis.'
property_tax_assess = {
        'title': property_tax_assess_title,
        'preview': property_tax_assess_pre,
        'explanation': 'The property may be re-evaluated on an annual basis. The Buyer and Seller agree not to hold each other responsible for any changes in the properties tax assessment.',
        'required': False
}

sales_tax_title = 'Sales Tax'
sales_tax_pre = 'If the sale of the Property (Real Property as described above) is subject to Sales Tax, then such tax shall be in addition to the Purchase Price. If the sale of the Property is not subject to SALES TAX, Seller agrees to certify on or before closing, that the sale of the Property is not subject to SALES TAX. Any SALES TAX on chattels, if applicable, is not included in the Purchase Price.'
sales_tax = {
        'title': sales_tax_title,
        'preview': sales_tax_pre,
        'explanation': 'If sales tax applies to the sale of the property, it shall be ADDED to the purchase price. If there is no sales tax, then the Seller agrees to provide documented proof before the completion date.',
        'required': False
}

notices_title = 'Notices'
notices_pre = 'Any notice relating hereto or provided for herein shall be in writing. The Seller consents and agrees that the Buyer, without further notice to Seller, may add Buyer’s spouse and/or Buyer’s children to the contract, if required by the Buyer’s financial intuition. The Buyer will provide notice as soon as possible to the Seller in writing, where all names are added to the contract. In addition to any provision contained herein and in any Additional Terms hereto, this offer, any counter-offer, notice of acceptance thereof or any notice to be given or received pursuant to this Agreement or any Additional Terms hereto (any of them, “Document”) shall be deemed given and received when delivered personally, electronically or hand delivered to the appropriate party (parties) provided in the Agreement, or where a facsimile number or email address is provided herein, when transmitted electronically, respectively, in which case, the signature(s) of the party (parties) shall be deemed to be original.'
notices = {
        'title': notices_title,
        'preview': notices_pre,
        'explanation': 'Any changes or notices concerning this agreement shall be delivered to the other party personally, in writing, or electronically.',
        'required': False
}

personal_information_title = 'Consumer Reports'
personal_information_pre = 'The Buyer is hereby notified that a consumer report containing credit and/or personal information may be referred to in connection with this transaction.'
personal_information = {
        'title': personal_information_title,
        'preview': personal_information_pre,
        'explanation': 'The Buyer’s consumer report may be referred to in this transaction (e.g. credit score).',
        'required': False
}

## ====================================================================

status_certificate_and_mgmt_title = 'Status Certificate and Management of Condominium'
status_certificate_and_mgmt_pre = 'The Seller represents and warrants to the Buyer that there are no special assessments contemplated by the Condominium Corporation, and there are no legal actions pending by or against or contemplated by the Condominium Corporation. The Seller consents to the Buyer’s or the Buyer’s authorized representative’s request for a Status Certificate from the Condominium Corporation. The Buyer acknowledges that a Management Agreement for the management of the condominium property may have been entered into by the Condominium Corporation. Copies of all current condominium documentation of the Condominium Corporation, including the Declaration, Description, By-laws, Common Element Rules and Regulations and the most recent financial statements of the Condominium Corporation is agreed by the Seller to be delivered by the Seller to the Buyer.'
status_certificate_and_mgmt = {
        'title': status_certificate_and_mgmt_title,
        'preview': status_certificate_and_mgmt_pre,
        'explanation': 'The Status certificate sets out the current status of the condominium corporation and the property. It includes copies of the Declaration, Bylaws, Rules, Financial Statements, Insurance, Reserve Fund Audits, to name a few.',
        'required': False
}

meetings_title = 'Meetings'
meetings_pre = '''The Seller warrants and represents to the Buyer that at the time of the acceptance of this Offer the Seller has not received a notice convening a special or general meeting of the Condominium Corporation respecting:
    (a) the termination of the government of the condominium property;
    (b) any substantial alteration in or 
    (c) substantial addition to the common elements or 
    (d) the renovation thereof; or
    (e) any substantial change in the assets or 
    (f) any substantial changes in the liabilities of the Condominium Corporation;
    and Seller covenants that if the Seller receives any such notice prior to the date of completion Seller shall forthwith notify the Buyer in writing and Buyer may thereupon at the Buyer’s option declare the Agreement terminated and all monies paid refunded in full to the Buyer  without interest or deduction.'''
meetings = {
        'title': meetings_title,
        'preview': meetings_pre,
        'explanation': 'The Seller must inform the buyer if any special meetings of the Condominium has taken place. For example, meetings concerning if the Condominium Corporation will be terminated, substantial additions or renovations and/or major changes to the finances of the Condominium.',
        'required': True
}

condo_laws_acknowledgement_title = 'Condo Laws Acknowledgement'
condo_laws_acknowledgement_pre = "The Buyer agrees to consent and acknowledge that the title to the Property is subject to the provisions of the Condominium Act and its conditions and provisions of the Declaration, Regulations and the terms, Description and Bylaws, Occupancy Standards Bylaws, including the Common Element Rules and other Rules and Regulations."
condo_laws_acknowledgement = {
        'title': condo_laws_acknowledgement_title,
        'preview': condo_laws_acknowledgement_pre,
        'explanation': 'The Buyer agrees to accept the title to the property subject to any applicable laws and rules on the usage of the property and municipal services (e.g. zoning bylaws, condominium corporation’s declaration, municipal agreements, etc.).',
        'required': False
}

condo_approval_of_agreement_title = 'Approval of the Agreement'
condo_approval_of_agreement_pre = 'In the event this Agreement of purchase and sale is conditional upon the consent of the Condominium Corporation or the Board of Directors, the Seller will apply forthwith for the requisite consent, and if such consent is refused, then this Agreement shall  be terminated and all monies paid returned in full without interest, deduction or other penalty to the Buyer.'
condo_approval_of_agreement = {
        'title': condo_approval_of_agreement_title,
        'preview': condo_approval_of_agreement_pre,
        'explanation': 'If it is necessary to obtain consent to the transaction from the Condominium Corporation or its Board of Directors then the Seller agrees to apply immediately for the consent. If the necessary consent is not received then the transaction is cancelled.',
        'required': True
}

condo_alterations_title = 'Alterations'
condo_alterations_pre = 'With respect to the unit, the seller represents and warrants that the condominium act, declaration, bylaws and rules of the condominium corporation have been complied with, and that no improvements, additions, alterations or repairs that require the consent of the condominium corporation have been executed in said unit, the exclusive use areas or the common elements, unless the required consent has been obtained from the condominium corporation. This warranty shall survive and not merge on the date of completion.'
condo_alterations = {
        'title': condo_alterations_title,
        'preview': condo_alterations_pre,
        'explanation': "The Seller warrants that any alterations, additions and improvements to the unit comply with the condominium corporation's rules and by-laws. If any consent was required for these changes, the Seller also warrants that the Condominium Corporation has consented to the unit changes.",
        'required': False
}

condo_documents_request_title = 'Requesting Documents'
condo_documents_request_pre = 'A request for the preparation or production of any title deed, abstract, survey or other evidence of title to the property by the Buyer, shall not be called for except such as are in the possession or control of the Seller. At the request of the Buyer, the Seller will deliver, if it is possible without incurring any costs in so doing, copies of all current condominium documentation of the Condominium Corporation, including the Declaration, Description, By-laws, Common Element Rules and Regulations and the most recent financial statements of the Condominium Corporation to Buyer immediately and prior to the Requisition Date.'
condo_documents_request = {
        'title': condo_documents_request_title,
        'preview': condo_documents_request_pre,
        'explanation': 'The Seller must provide the Buyer with any information concerning the property that is evidence of title. The Seller will provide such information to the Buyer upon request immediately and prior to the completion date (e.g. survey and deed).',
        'required': True
}

condo_discharge_title = 'Discharge'
condo_discharge_pre = 'If a discharge of any Charge/Mortgage held by a corporation incorporated pursuant to the Trust And Loan Companies Act (Canada), Chartered Bank, Trust Company, Credit Union, Caisse Populaire or Insurance Company and which is not to be assumed by Buyer on completion, is not available in registrable form on completion, Buyer agrees to accept Seller’s lawyer’s personal undertaking to obtain, out of the closing funds, a discharge in registrable form and to register same, or cause same to be registered, on title within a reasonable period of time after completion, provided that on or before completion Seller shall provide to Buyer a mortgage statement prepared by the mortgagee, lienholder or encumbrancer  setting out the balance required to obtain the discharge, and, where a real-time electronic cleared funds transfer system is not being used, a direction executed by Seller directing payment to the mortgagee, lienholder or encumbrancer  of the amount required to obtain the discharge out of the balance due on completion.'
condo_discharge = {
        'title': condo_discharge_title,
        'preview': condo_discharge_pre,
        'explanation': 'If the Seller has a mortgage with a chartered bank, trust company, insurance company, credit union or Caisse Populaire, it will most likely not be discharged on or before the completion date. In this case the Buyer will receive from the Seller a mortgage statement disclosing the discharge amount and the discharge date. All other mortgages will have to be discharged by closing.',
        'required': True
}

condo_adjustments_title = 'Adjustments'
condo_adjustments_pre = "The Buyer shall assume any common expenses; realty taxes, including local improvement rates; mortgage interest; rentals; unmetered public or private utilities and fuel where billed to the Unit and not the Condominium Corporation; are to be apportioned to the Buyer and allowed to the date of completion. There shall be no adjustment for the Seller's share of any assets or liabilities of the Condominium Corporation including any reserve or contingency fund to which Seller may have contributed prior to the date of completion."
condo_adjustments = {
        'title': condo_adjustments_title,
        'preview': condo_adjustments_pre,
        'explanation': 'All additional property expenses, such as rent, mortgage interest, taxes, and utility payments, on the completion date and after the completion date, will be applicable to the Buyer, will be paid by the Buyer. All expenses before the completion date, will be paid by the Seller.',
        'required': False
}

unit_insurance_title = 'Insurance'
unit_insurance_pre = 'The Unit and all other things being purchased shall be and remain at the risk of the Seller until the date of completion. In the event of substantial damage to the Property Buyer may at Buyer’s option either permit the proceeds of insurance to be used for repair of such damage in accordance with the provisions of the Insurance Trust Agreement, or either this offer shall be null and void and all the monies paid returned without interest or deduction to the Buyer, or else the Buyer take the proceeds of any insurance and complete the purchase. Buyer shall supply Seller with reasonable evidence of adequate insurance if Seller is taking back a Charge/ Mortgage, or Buyer is assuming a Charge/Mortgage, in order to protect Seller’s or other mortgagee’s interest on the date of completion.'
unit_insurance = {
        'title': unit_insurance_title,
        'preview': unit_insurance_pre,
        'explanation': 'The Seller is responsible for the property until closing and must maintain insurance until completion. In the event of substantial damage to the property, the Buyer can cancel the Agreement, or can close and get the proceeds of any insurance.',
        'required': True
}

alt_document_prep_title = 'Document Preparation'
alt_document_prep_pre = 'The Transfer/Deed shall, save for the Land Transfer Tax Affidavit, be prepared in registrable form at the expense of Seller, and any Charge/Mortgage to be given back by the Buyer to Seller at the expense of the Buyer.'
alt_document_prep = {
        'title': alt_document_prep_title,
        'preview': alt_document_prep_pre,
        'explanation': 'The deed/ transfer will be registered at the Seller’s expense (except the land transfer tax affidavit) and any mortgage given to the Buyer is at the Buyer’s expense.',
        'required': False
}

alt_residency_title = 'Residency'
alt_residency_pre = "Buyer shall be credited towards the Purchase Price with the amount, if any, necessary for Buyer to pay to the Minister of National Revenue to satisfy Buyer's liability in respect of tax payable by Seller under the non-residency provisions of the Income Tax Act by reason of this sale. Buyer shall not claim such credit if Seller delivers on or prior to the date of completion the prescribed certificate or a statutory declaration that Seller is not then a non-resident of Canada."
alt_residency = {
        'title': alt_residency_title,
        'preview': alt_residency_pre,
        'explanation': 'Non-residents must pay different taxes than residences, as such residency must be disclosed during this transaction.',
        'required': False
}

co_documentation_title = 'Corporation Documentation'
co_documentation_pre = '''On or prior to closing the Seller shall deliver to the Buyer:
    (1) a certified copy of the Resolution of the Board of Directors of the Corporation approving the Buyer as a shareholder and as an occupant of the Unit;
    (2) a share certificate for the Seller’s shares in the capital of the Corporation endorsed in favour of the Buyer.
    (3) a certificate or letter from the Corporation confirming:
    (a) with respect to the Property, that all charges and obligations have been paid or discharged as of the date of closing;
    (b) with respect to the Corporation that the affairs of the Corporation are in order and that there are no legal actions pending against the Corporation or contemplated by the Corporation, that there are no special assessments contemplated by the Corporation, that there are no orders or complaints against the real property by the Building, Health or Fire Departments, that no sale of real property is contemplated, and the Building is not and never has been insulated with Urea-Formaldehyde Foam Insulation or Vermiculite.'''
co_documentation = {
        'title': co_documentation_title,
        'preview': co_documentation_pre,
        'explanation': 'The Seller must provide the Buyer with every document concerning the property and the Corporation. The Seller will provide such information to the Buyer prior to the completion date (e.g. Resolution of the Board of Directors, Share Certificate, Confirmation Certificate, etc. ).',
        'required': True
}

co_meetings_title = 'Meetings'
co_meetings_pre = '''Seller represents and warrants to Buyer that at the time of the acceptance of this Offer the Seller has not received a notice convening a special or general meeting of the Corporation respecting;
(a) the termination of the government of the property; 
(b) the winding up or dissolution of the Corporation; 
(c) any substantial alteration in or
(d) substantial addition to the property or 
(e) the renovation thereof; or 
(f) any substantial change in the assets or 
(g) any substantial change in the liabilities of the Corporation;
and Seller covenants that if the Seller receives any such notice prior to the date of completion the Seller shall forthwith notify Buyer in writing and the Buyer may thereupon at the Buyer’s option declare this Agreement to be terminated and all monies paid returned in full without interest or deduction to the Buyer.'''
co_meetings = {
        'title': co_meetings_title,
        'preview': co_meetings_pre,
        'explanation': 'The Seller must inform the buyer if any special meetings of the Condominium has taken place. For example, meetings concerning if the Condominium Corporation will be terminated, substantial additions or renovations and/or major changes to the finances of the Condominium.',
        'required': True
}

co_title_title = 'Title'
co_title_pre = "Buyer agrees to accept the Corporation's title to the Property subject to all rights and easements registered against title for the supply and installation of telephone services, electricity, gas, sewers, water, television cable facilities and other related services; provided that title to the Property is otherwise good and free from all encumbrances except: (a) as herein expressly provided; (b) any registered restrictions, conditions or covenants that run with the land provided such have been complied with; and (c) any registered municipal agreements and registered agreements with publicly regulated utilities providing such have been complied with, or security has been posted to ensure compliance and completion, as evidenced by a letter from the relevant municipality or regulated utility;(d) any existing municipal agreements, zoning by-laws and/or regulations and utility or service contracts. (e) any minor easements for the supply of domestic utility or telephone services to the property or adjacent properties; (f) any easements for drainage, storm or sanitary sewers, public utility lines, telephone lines, cable television lines or other services which do not materially affect the use of the property; If by the Completion Date (Requisition Date) any valid objection to title or to any outstanding work order or deficiency notice, or to the fact the said present use may not lawfully be continued, or that the principal building may not be insured against risk of fire is made in writing to Seller and which Seller is unable or unwilling to remove, remedy or satisfy or obtain insurance save and except against risk of fire (Title Insurance) in favour of the Buyer and any mortgagee, (with all related costs at the expense of the Seller), and which Buyer will not waive, this Agreement notwithstanding any intermediate acts or negotiations in respect of such objections, shall be at an end and all monies paid shall be returned without interest or deduction. Save as to any valid objection so made by such day and except for any objection going to the root of the title, Buyer shall be conclusively deemed to have accepted Seller’s title to the property."
co_title = {
        'title': co_title_title,
        'preview': co_title_pre,
        'explanation': 'The Buyer agrees to abide by all the condominiums rules and terms, upon completion of the transaction.',
        'required': False
}

co_loan_discharge_title = 'Loan Discharge'
co_loan_discharge_pre = "If a discharge of any Charge, lien or other encumbrance held by a corporation incorporated pursuant to the Trust And Loan Companies Act (Canada), Chartered Bank, Trust Company, Credit Union, Caisse Populaire or Insurance Company and which is not to be assumed by Buyer on completion, is not available in registrable form on completion, Buyer agrees to accept Seller's lawyer's personal undertaking to obtain, out of the closing funds, a discharge in registrable form and to register same, or cause same to be registered, on title within a reasonable period of time after completion, provided that on or before completion Seller shall provide to Buyer a statement prepared by the mortgagee, lienholder or encumbrancer setting out the balance required to obtain the discharge, and, where a real-time electronic cleared funds transfer system is not being used, a direction executed by Seller directing payment to the mortgagee, lienholder or encumbrancer of the amount required to obtain the discharge out of the balance due on completion."
co_loan_discharge = {
        'title': co_loan_discharge_title,
        'preview': co_loan_discharge_pre,
        'explanation': 'If the Seller has a mortgage with a chartered bank, trust company, insurance company, credit union or Caisse Populaire, it will most likely not be discharged on or before the completion date. In this case the Buyer will receive from the Seller a mortgage statement disclosing the discharge amount and the discharge date. All other mortgages will have to be discharged by closing.',
        'required': False
}

maintenance_pre = 'The Seller agrees to leave the premises, including the floors, in a clean and broom swept condition. The Seller agrees to clean, repair or replace any damaged floor covering in the building and permit the Buyer the right to inspect the premises to ensure that said cleaning, repairing or replacing has been completed. The Seller agrees to remove all equipment, storage containers and any other materials, including refuse and debris, from the property and to leave the parking area in a clean and vacant condition.'
maintenance_gen = 'Maintenance Clause'
maintenance = {
        'preview': maintenance_pre,
        'generator': maintenance_gen,
        'explanation': 'The Seller agrees to ensure the entire property is under proper maintenance until the completion date. All damaged components shall be fixed or replaced, and the property shall be in a clean and uncluttered state. To avoid later disputes, the Buyer should inspect the property prior to closing to ensure the property is in a satisfactory state as per this agreement.',
        'required': False
}

co_adjustments_title = 'Adjustments'
co_adjustments_pre = "The Buyer shall assume maintenance expenses and, where billed to the Unit and not the Corporation, realty taxes, including local improvement rates; interest; rentals; unmetered public or private utilities and fuel; are to be apportioned to the Buyer and allowed to the date of completion. There shall be no adjustment for the Seller's share of any reserve or contingency fund to which the Seller may have contributed prior to the date of completion."
co_adjustments = {
        'title': co_adjustments_title,
        'preview': co_adjustments_pre,
        'explanation': 'All additional property expenses, such as rent, mortgage interest, taxes, and utility payments, on the completion date and after the completion date, will be applicable to the Buyer and will be paid by the Buyer. All expenses before the completion date, will be paid by the Seller.',
        'required': False
}


alt_alterations_title = 'Alterations'
alt_alterations_pre = 'With respect to the unit, the seller represents and warrants that the act, declaration, bylaws and rules of the corporation have been complied with, and that no improvements, additions, alterations or repairs that require the consent of the corporation has been executed in the said unit, the exclusive use areas or the common elements, unless the required consent has been obtained from the corporation. This warranty shall survive and not merge on the date of completion.'
alt_alterations = {
        'title': alt_alterations_title,
        'preview': alt_alterations_pre,
        'explanation': "The Seller warrants that any alterations, additions and improvements to the unit comply with the condominium corporation's rules and by-laws. If any consent was required for these changes, the Seller also warrants that the Condominium Corporation has consented to the unit changes.",
        'required': False
}

occupancy_agreement_title = 'Occupancy Agreement'
occupancy_agreement_pre = 'The Buyer agrees on or prior to closing to enter into an Occupancy Agreement with the Corporation and to abide by the rules and regulations of the Corporation.'
occupancy_agreement = {
        'title': occupancy_agreement_title,
        'preview': occupancy_agreement_pre,
        'explanation': 'The Buyer agrees to enter into an Occupancy agreement with the Corporation and to follow all the rules and regulation.',
        'required': False
}

alt_documents_request_title = 'Requesting Documents'
alt_documents_request_pre = 'A request for the preparation or production of any title deed, abstract, survey or other evidence of title to the property by the Buyer, shall not be called for except such as are in the possession or control of the Seller. At the request of the Buyer, the Seller will deliver any sketch or survey of the property within Seller’s control to Buyer immediately and prior to the Requisition Date.'
alt_documents_request = {
        'title': alt_documents_request_title,
        'preview': alt_documents_request_pre,
        'explanation': 'The Seller must provide the Buyer with any information concerning the property that is evidence of title. The Seller will provide such information to the Buyer upon request immediately and prior to the completion date (e.g. survey and deed).',
        'required': True
}

cw_residency_title = 'Residency'
cw_residency_pre = "Buyer shall be credited towards the Purchase Price with the amount, if any, necessary for Buyer to pay to the Minister of National Revenue to satisfy Buyer's liability in respect of tax payable by Seller under the non-residency provisions of the Income Tax Act by reason of this sale. Buyer shall not claim such credit if Seller delivers on or prior to the date of  completion the prescribed certificate or a statutory declaration that Seller is not then a non-resident of Canada."
cw_residency = {
        'title': cw_residency_title,
        'preview': cw_residency_pre,
        'explanaton': 'Non-residents must pay different taxes than residences, as such residency must be disclosed during this transaction.',
        'required': False
}

cw_adjustments_title = 'Adjustments'
cw_adjustments_pre = "The buyer shall assume maintenance expenses and, where billed to the Unit and not the Corporation, realty taxes, including local improvement rates; mortgage interest; rentals; unmetered public or private utilities and fuel; are to be apportioned to the Buyer and allowed to the date of completion. There shall be no adjustment for the Seller's share of any reserve or contingency fund to which the Seller may have contributed prior to the date of completion."
cw_adjustments = {
        'title': cw_adjustments_title,
        'preview': cw_adjustments_pre,
        'explanation': 'All additional property expenses, such as rent, mortgage interest, taxes, and utility payments, on the completion date and after the completion date, will be applicable to the Buyer, will be paid by the Buyer. All expenses before the completion date, will be paid by the Seller.',
        'required': False
}

m_rules_and_regs_title = 'Rules and Regulations'
m_rules_and_regs_pre = 'The Buyer acknowledges that the Land lease may include Rules and Regulations for the occupancy of the Land and the Buyer agrees to accept and comply with said Rules and Regulations.'
m_rules_and_regs = {
        'title': m_rules_and_regs_title,
        'preview': m_rules_and_regs_pre,
        'explanation': 'The Buyer agrees to follow any rules and regulations tied to the usage of the property and the land lease.',
        'required': False
}

m_lease_title = 'Lease'
m_lease_pre = 'The Buyer acknowledges that Dwelling is currently situated upon the Land pursuant to a Lease as more particularly set out in Additional Terms attached hereto. The Seller agrees to assign the Seller’s interest in the Lease to the Buyer and the Buyer agrees to accept the assignment of the Lease. If the said Lease contains a provision requiring that the Landlord consent to the assignment of the Lease, then Seller will apply forthwith for the requisite consent, and provide a copy in writing of the consent, and if such consent is refused and the Buyer does not enter into a new lease agreement with the Landlord, then this Agreement this offer shall be terminated and all monies paid returned in full without interest, deduction or other penalty to the Buyer. The Buyer agrees to cooperate and provide such information and documentation as may be within control of the Buyer in order to obtain said assignment of Lease.'
m_lease = {
        'title': m_lease_title,
        'preview': m_lease_pre,
        'explanation': 'The Buyer acknowledge that the property is on a leased land and the seller agrees to assign this lease to the Buyer. If the Seller requires consent to transfer this lease to the Buyer, then the Buyer will get this consent immediately, if not then this agreement is cancelled.',
        'required': False
}

m_title_title = 'Title'
m_title_pre = 'Seller hereby consents to the Landlord of the Land, the municipality or other governmental agencies releasing to Buyer details of all outstanding work orders, deficiency notices and all matters affecting the Dwelling, and Seller agrees to execute and deliver such further authorizations in this regard as Buyer may reasonably require. Buyer shall be allowed until the Completion Date (Requisition Date), to examine the title to the Dwelling at the Buyer’s own expense, to satisfy Buyer that there are no outstanding work orders, deficiency notices or other matters affecting the Dwelling, and that its present use may be lawfully continued and that the principal building may be insured against risk of fire. If by the Completion Date (Requisition Date) any valid objection to title or to any outstanding work order or deficiency notice, or to the fact the said present use may not lawfully be continued, or that the Dwelling may not be insured against risk of fire is made in writing to Seller and which Seller is unable or unwilling to remove, remedy or satisfy or obtain insurance save and except against risk of fire in favour of the Buyer and any mortgagee, (with all related costs at the expense of the Seller), and which Buyer will not waive, this Agreement notwithstanding any intermediate acts or negotiations in respect of such objections, shall be at an end and all monies paid shall be returned without interest or deduction and Seller shall not be liable for any costs. Save as to any valid objection so made by such day and except for any objection going to the root of the title, Buyer shall be conclusively deemed to have accepted Seller’s title to the Dwelling.'
m_title = {
        'title': m_title_title,
        'preview': m_title_pre,
        'explanation': 'The Seller will grant the Buyer access to all title information concerning the property. The Seller will provide any government documents to the Buyer upon request, such as work orders. Seller must fix any issues that arise from this search, or this agreement is canceled.',
        'required': True
}

m_documents_request_title = 'Requesting Documents'
m_documents_request_pre = "A request for the preparation or production of any prior Bills of Sale or other evidence of title to the Dwelling by the Buyer, shall not be called for except such as are in the possession or control of Seller. At the request of the Buyer, Seller will deliver any sketch or plans of the Dwelling, including informational material from the manufacturer, within Seller's control to Buyer as soon as possible and prior to the Requisition Date."
m_documents_request = {
        'title': m_documents_request_title,
        'preview': m_documents_request_pre,
        'explanation': 'The Seller must provide the Buyer with any information concerning the property that is evidence of title. The Seller will provide such information to the Buyer upon request immediately and prior to the completion date (e.g. survey and deed).',
        'required': True
}

m_discharge = {
        'title': 'Discharge',
        'preview': "If a discharge of any security interest held by a corporation incorporated pursuant to the Trust And Loan Companies Act (Canada), Chartered Bank, Trust Company, Credit Union, Caisse Populaire or Insurance Company and which is not to be assumed by Buyer on completion, is not available in registrable form on completion, Buyer agrees to accept Seller's lawyer's personal undertaking to obtain, out of the closing funds, a registrable discharge and to register same, or cause same to be registered within a reasonable period of time after completion, provided that on or prior to the date of  completion Seller shall provide to Buyer a statement prepared by the security interest holder setting out the balance required to obtain the discharge, and, where a real-time electronic cleared funds transfer system is not being used, a direction executed by Seller directing payment to the holder of the amount required to obtain the discharge out of the balance due on the date of completion.",
        'explanation': 'If the Seller has a mortgage with a chartered bank, trust company, insurance company, credit union or Caisse Populaire, it will most likely not be discharged on or before the completion date. In this case the Buyer will receive from the Seller a mortgage statement disclosing the discharge amount and the discharge date. All other mortgages will have to be discharged by closing.',
        'required': False
}

m_inspection = {
        'title': 'Inspection',
        'preview': 'Buyer hereto consents and agrees to  having had the opportunity to inspect the Dwelling and understands that upon acceptance of this offer there shall be a binding agreement of purchase and sale between the parties in this Agreement.',
        'explanation': 'The Buyer acknowledges that they had the opportunity to inspect the property utilizing the services of a professional inspector. The Buyer also acknowledges the importance of a property inspection and still chooses not to have one done on the property.',
        'required': False
}

m_insurance = {
        'title': 'Insurance',
        'preview': "The Dwelling and all buildings on the Land and all other things being purchased shall be and remain until the date of completion at the risk of Seller. Pending completion, all insurance policies, if any, shall be held by the Seller and the proceeds thereof in trust for the Buyer and Seller as their interests may appear and in the event of substantial damage,  either this offer shall be null and void and all the monies paid returned without interest or deduction or else the Buyer take the proceeds of any insurance and complete the purchase. No insurance shall be transferred on completion. If Seller is taking back a Security Interest, or Buyer is assuming a Security Interest, Buyer shall supply Seller with reasonable evidence of adequate insurance to protect Seller's or other security holder's interest on or prior to the date of completion.",
        'explanation': 'The Seller is responsible for the property until closing and must maintain insurance until completion. In the event of substantial damage to the property, the Buyer can cancel the Agreement, or can close and get the proceeds of any insurance.',
        'required': True
}

m_document_prep = {
        'title': 'Document Preparation',
        'preview': 'The Bill of Sale shall be prepared in registrable form at the expense of Seller, and any Security Interest to be given back by the Buyer to Seller at the expense of the Buyer.',
        'explanation': 'The Bill of Sale will be registered at the Seller’s expense and any Security Interest given to the Buyer is at the Buyer’s expense.',
        'required': True
}


# These clauses are immutable, and belong to every non-rental contract.
STATIC_CLAUSES = {
        'completion_date_adjustments': completion_date_adjustments,
        'title_search': title_search,
        'title': title,
        'documents_request': documents_request,
        'discharge': discharge,
        'inspection_omit': inspection_omit,
        'insurance': insurance,
        'planning': planning,
        'document_prep': document_prep,
        'residency': residency,
        'non_residency': non_residency,
        'adjustments': adjustments,
        'property_tax_assessment': property_tax_assess,
        'deadline_extensions': deadline_extensions,
        'tender': tender,
        'family_law_act': family_law,
        'personal_information': personal_information,
        'agreement_in_writing': agreement_in_writing,
        'time_and_date': time_and_date,
        'electronic': electronic,
        'sales_tax': sales_tax,
        'notices': notices,
        'buyer_negligence': buyer_negligence,

        ## ====================================================================
        
        'status_certificate_and_mgmt': status_certificate_and_mgmt,
        'meetings': meetings,
        'condo_laws_acknowledgement_pre': condo_laws_acknowledgement,
        'unit_insurance': unit_insurance,
        'alt_document_prep': alt_document_prep,
        'alt_residency': alt_residency,
        'alt_alterations': alt_alterations,
        'occupancy_agreement': occupancy_agreement,
        'alt_documents_request': alt_documents_request,
}

CONDO_STATIC_CLAUSES = {
        'approval_of_agreement': condo_approval_of_agreement,
        'alterations': condo_alterations,
        'documents_request': condo_documents_request,
        'discharge': condo_discharge,
        'adjustments': condo_adjustments,
}

COOP_STATIC_CLAUSES = {
        'corporation_documentation': co_documentation,
        'meetings': co_meetings,
        'title': co_title,
        'loan_discharge': co_loan_discharge,
        'adjustments': co_adjustments,
}

COOWNERSHIP_STATIC_CLAUSES = {
        'residency': cw_residency,
        'adjustments': cw_adjustments,
}

MOBILE_STATIC_CLAUSES = {
        'rules_and_regs': m_rules_and_regs,
        'lease': m_lease,
        'title': m_title,
        'documents_request': m_documents_request,
        'discharge': m_discharge,
        'inspection': m_inspection,
        'insurance': m_insurance,
}

