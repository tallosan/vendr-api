# -*- coding: utf-8 -*-


# Fields: Deposit amount, Seller name, Deposit Deadline.
deposit = {
        'preview': 'Buyer submits upon acceptance {} Dollars (CDN $) by negotiable cheque payable to {} to be held in trust pending completion or other termination of this Agreement and will form part of the Purchase Price on completion. “Upon Acceptance” shall mean that the Buyer is required to deliver the deposit to the Deposit Holder within {} days of the acceptance of this Agreement, for the purpose of this Agreement. In the event the Buyer fails to pay the Deposit as required by this Agreement, the Seller may, at the Seller’s option, terminate this Contract. The Buyer and Seller hereby acknowledge that the Deposit Holder is authorized to place the deposit in trust in the Seller’s Solicitor/ Conveyancer trust account or in the Deposit Holder’s non-interest bearing trust account and no interest shall be earned, received or paid on the deposit, unless otherwise provided for in this Agreement. If the sale does not complete, the Deposit shall be returned to such party as stakeholder or paid into Court.'.decode('utf-8'),
	'explanation': 'A buyer submits a deposit on the home to show their intent to purchase, once the offer is accepted. A time is set to deliver the deposit to ensure the Buyer shows their intent as soon as possible. The deposit also acts as a partial payment for the purchase. If the agreement is canceled the deposit is returned.'
}

irrevocability= { 'preview': 'This offer shall be irrevocable by the Buyer and Seller until {} on the day of {}, after which time, if not accepted, this offer shall be null and void and the deposit shall be refunded to the Buyer in full without interest or deduction.'.decode('utf-8'),
	'explanation': 'The party (Buyer/Seller) submitting an Offer to the other side agrees to allow the other side (Buyer/Seller) accept the offer by the specified deadline. The submitting party cannot cancel the offer prior to this deadline. Before the offer expiration date specified below, this offer can be accepted by the other side at anytime.'
}

# Fields: List of chattels included.
chattels_inc= { 'preview': 'Unless otherwise stated in this Agreement or any Additional Terms hereto, Seller agrees to convey all fixtures and chattels included in the Purchase Price free from all liens, encumbrances or claims affecting the said fixtures and chattels.\n{}'.decode('utf-8'),
	'explanation': 'The parties must list the items that the Buyer wishes to include in the Purchase price. This section is for moveable possessions such as fridges, stoves and other items that are not attached to the property. To avoid disputes later in the transaction, the items should have detail descriptions. (e.g. GE stove, Kenmore Refrigerator or even item serial numbers).'
}

# Fields: List of fixtures excluded.
fixtures_exc= { 'preview': '{}'.decode('utf-8'),
	'explanation': 'The parties must list the items excluded from the Purchase price. This section is for immovable possessions such as water heaters, dining room light fixtures  and other items that are attached to the property. To avoid disputes later in the transaction, the items should have detail descriptions (e.g. item serial numbers or GE furnace).'
}

# Fields: List of rented items.
rented_items= { 'preview': 'The following equipment is rented and excluded in the Purchase Price. The Buyer agrees to assume the rental contract(s), if assumable:\n{}\nThe Buyer agrees to co-operate and execute such documentation, records and reports as may be required to facilitate such assumption.'.decode('utf-8'),
	'explanation': 'The parties must list the rental items that the Buyer agrees to lease and is excluded from the Purchase price. This section is for possessions such as water heaters and other rental items. To avoid disputes later in the transaction, the items should have detail descriptions (e.g. item serial numbers or GE furnace).'
}

# Fields: The date the mortgage is due.
mortgage_date= { 'preview': 'Unless the Buyer gives notice in writing delivered to the Seller personally or in accordance with any other provisions for the delivery of notice in this Agreement or any Additional Terms thereto, by mutual agreement in writing the Buyer must arrange the aforementioned Charge/Mortgage not later than {}, that the Buyer has arranged, at the Buyer’s own expense, Charge/ Mortgage satisfactory to pay the balance of the purchase price, this offer shall be terminated and all monies paid refunded in full without interest or deduction to the Buyer. This condition is included for the benefit of the Buyer and may be waived at the Buyer’s sole option by notice in writing to the Seller as aforesaid within the time period stated herein.'.decode('utf-8'),
        'explanation': 'This Offer is conditional upon the Buyer arranging, at the Buyer’s own expense, Charge/ Mortgage satisfactory to pay the balance of the purchase price. Unless the Buyer gives notice in writing delivered to the Seller personally or in accordance with any other provisions for the delivery of notice in this Agreement or any Additional Terms thereto, by mutual agreement in writing the Buyer must arrange the aforementioned Charge/Mortgage not later than [AGREED UPON DATE BY BOTH PARTIES], that this condition is fulfilled, this offer shall be terminated and all monies paid refunded in full without interest or deduction to the Buyer. This condition is included for the benefit of the Buyer and may be waived at the Buyer’s sole option by notice in writing to the Seller as aforesaid within the time period stated herein.\nWarning: The majority of home buyers require a mortgage in order to afford the purchase of a home. It is in the best interest of the Buyer and Seller for the Buyer to acquire a mortgage that covers the full purchase price.'
}

survey_date= { 'preview': 'The Seller agrees to provide, at the Seller’s own expense, not later than {}, an existing survey or new survey by a professional Land Surveyor, of said property showing the current location of all structures, buildings fences, improvements, easements, rights of way, and encroachments affecting said property. The Seller also agrees to supply all building plans, mechanical drawings, any other plans, and all warranties and services manuals, if available, applicable to any equipment or chattels included in the purchase price. The Seller will further deliver, on completion, a declaration confirming that there have been no additions to the structures, buildings, fences, and improvements on the property since the date of this survey.'.decode('utf-8'),
        'explanation': 'The Seller agrees to give the Buyer an existing survey of the property, or a new survey by a professional land Surveyor, by the date specified. All building plans, property manuals and other plans should also be given to the Buyer. To avoid later disputes, the Buyer should inspect these documents prior to closing, to ensure the property is in a satisfactory state, as per this agreement.\nWarning: The size of the lot, the fencing boundaries and even the improvements permitted on the land, are all on the survey, among other factors. This will protect the Buyer from purchasing properties with unlawful improvements and other survey violations. This clause protects the Buyer and Seller against from future legal liability.'
}

completion_date= { 'preview': 'This Agreement shall be completed by no later than the {} day of the {} month of the year {}. Upon completion, the Buyer will have vacant possession of the property unless otherwise provided for in this Agreement. The Seller warrants and represents that  the Seller has obtained a release from any prior Agreement of Purchase and Sale.'.decode('utf-8'),
	'explanation': 'The completion date is the date the Buyer takes possession of the property and a lawyer has registered the ownership transfer of the property. Unless there are terms in writing stating otherwise, the Seller is to vacant the property by this date.'
}

chattels_and_fixs= { 'preview': 'The Seller represents and warrants that the chattels and fixtures as included in this Agreement will be in good working order and free from liens and encumbrances on completion. The parties in this Agreement of Purchase and Sale agree that this representation and warranty shall survive and not merge on completion of this transaction, but apply only to those circumstances existing at the date of completion stated herein.'.decode('utf-8'),
	'explanation': 'All the Chattels (moveable possessions, such as fridges) and Fixtures (immovable possessions, such as water heaters) listed in this agreement, must be in good working order by the completion date. There should also be no legal claim(s) against any of the specified possessions in this Agreement.'
}

buyer_mrtg_arrange= { 'preview': 'This Offer is conditional upon the Buyer arranging, at the Buyer’s own expense, Charge/ Mortgage satisfactory to pay the balance of the purchase price. This condition is included for the benefit of the Buyer and may be waived at the Buyer’s sole option by notice in writing to the Seller as aforesaid within the time period stated herein.'.decode('utf-8'),
        'explanation': 'The Buyer must acquire a loan/mortgage that is enough to pay the full price minus the deposit and downpayment, by the date specified. To avoid later disputes, the Buyer should provide the Seller the Mortgage information, along with copies for the Buyer’s lawyer.\nWarning: Majority of home buyers require a mortgage in order to afford the purchase of a home. It is in the best interest of the Buyer and Seller for the Buyer to acquire a mortgage that covers the full purchase price.'
}

# Fields: None.
equipment= { 'preview': 'The Seller warrants and represents that all the mechanical, electrical, heating, ventilation, air conditioning systems, air compressors, elevators, conveyor systems, sprinkler systems, boilers, and all the other equipment on the real property shall be in good working order on completion. The Buyer and Seller agree that this warranty shall survive and not merge on the date of completion, but apply only to the state of the property at the date of completion stated herein.'.decode('utf-8'),
	'explanation': 'All the Equipment that is part of the property, must be in good working order by the completion date (e.g. Sprinkler system, air conditioning system, electricity, etc.).'
}

# Fields: None.
environmental= { 'preview': 'The seller represents and warrants that all environmental laws and regulations have been complied with, no hazardous conditions or substances exist on the land, no limitations or restrictions affecting the continued use of the property exist, other than those specifically provided for herein, with respect to environmental matters said environmental matters are not subject to any pending litigation, and no charges or prosecutions respecting environmental matter exist, there has been no prior use as a waste disposal site, no portion of the property has been designated as hazard land, floodplain, or an environmentally protected zone and all applicable licenses are in force. The Seller agrees to provide to the Buyer upon request, access to all documents, records and reports relating to environmental matters in possession of the Seller. The Seller further authorizes the appropriate Ministry, to release to the Buyer or the Buyer’s Solicitor, any and all information that may be on record in the Ministry office with respect to the said property. The parties in this Agreement agree that this representation and warranty shall survive and not merge on the date of completion of this transaction, but apply only to those circumstances existing at the date of completion. This condition is included for the benefit of the Buyer and may be waived at the Buyer’s sole option by notice in writing to the Seller as aforesaid within the time period stated herein.'.decode('utf-8'),
	'explanation': 'The Seller must ensure all environmental laws and regulations are followed by the completion date. If there are any environmental issues (e.g. hazardous substances, soil contamination, etc.), the Seller must fix them by the completion date.'
}

# Fields: None
maintenance= { 'preview': 'The Seller agrees to leave the premises, including the floors, in a clean and broom swept condition. The Seller agrees to clean, repair or replace any damaged floor covering in the building and permit the Buyer the right to inspect the premises to ensure that said cleaning, repairing or replacing has been completed. The Seller agrees to remove all equipment, storage containers and any other materials, including refuse and debris, from the property and to leave the parking area in a clean and vacant condition.'.decode('utf-8'),
	'explanation': 'The Seller agrees to ensure the entire property is under proper maintenance until the completion date. All damaged components shall be fixed or replaced, and the property shall be in a clean and uncluttered state. To avoid later disputes, the Buyer should inspect the property prior to closing to ensure the property is in a satisfactory state as per this agreement.'
}

uffi= { 'preview': 'Seller represents and warrants to Buyer that during the time Seller has owned the property, the Seller has not caused any building on the property to be insulated with insulation containing urea formaldehyde, vermiculite and/or any other hazardous substance which materially affects the use of the property, and that to the best of Seller’s knowledge no building on the property contains or has ever contained insulation that contains urea formaldehyde, vermiculite and/or other hazardous substance, which materially affects the use of the property. This warranty shall survive and not merge on the date of completion, and if the building is part of a multiple unit building, this warranty shall only apply to that part of the building which is the subject of this transaction.'.decode('utf-8'),
	'explanation': 'The Seller warrants that they have not installed any Urea Formaldehyde Foam Insulation and/or Vermiculite insulation, and to the best of their knowledge there is none in the property being purchased in this agreement.'
}

payment_method = { 'preview': 'The Buyer agrees to pay the Seller on completion of this transaction via a {} payment.',
        'explanation': 'The Buyer agrees to pay the the full purchase price using the selected payment method.'
}

DYNAMIC_STANDARD_CLAUSES = {
        'deposit': deposit,
        'irrevocability': irrevocability,
        'chattels_inc': chattels_inc,
        'fixtures_exc': fixtures_exc,
        'rented_items': rented_items,
        'mortgage_date': mortgage_date,
        'survey_date': survey_date,
        'completion_date': completion_date,
        'chattels_and_fixs': chattels_and_fixs,
        'buyer_mrtg_arrange': buyer_mrtg_arrange,
        'equipment': equipment,
        'environmental': environmental,
        'maintenance': maintenance,
        'uffi': uffi,
        'payment_method': payment_method
}

