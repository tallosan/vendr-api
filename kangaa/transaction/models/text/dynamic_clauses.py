# -*- coding: utf-8 -*-


# Fields: Deposit amount, Seller name, Deposit Deadline.
deposit = ('Buyer submits upon acceptance {} Dollars (CDN $) by negotiable cheque payable to {} to be held in trust pending completion or other termination of this Agreement and will form part of the Purchase Price on completion. “Upon Acceptance” shall mean that the Buyer is required to deliver the deposit to the Deposit Holder within {} days of the acceptance of this Agreement, for the purpose of this Agreement. In the event the Buyer fails to pay the Deposit as required by this Agreement, the Seller may, at the Seller’s option, terminate this Contract. The Buyer and Seller hereby acknowledge that the Deposit Holder is authorized to place the deposit in trust in the Seller’s Solicitor/ Conveyancer trust account or in the Deposit Holder’s non-interest bearing trust account and no interest shall be earned, received or paid on the deposit, unless otherwise provided for in this Agreement. If the sale does not complete, the Deposit shall be returned to such party as stakeholder or paid into Court.').decode('utf-8')

irrevocability = ('This offer shall be irrevocable by the Buyer and Seller until {} on the day of {}, after which time, if not accepted, this offer shall be null and void and the deposit shall be refunded to the Buyer in full without interest or deduction.').decode('utf-8')

# Fields: List of chattels included.
chattels_inc = ('Unless otherwise stated in this Agreement or any Additional Terms hereto, Seller agrees to convey all fixtures and chattels included in the Purchase Price free from all liens, encumbrances or claims affecting the said fixtures and chattels.\n{}').decode('utf-8')

# Fields: List of fixtures excluded.
fixtures_exc = ('{}').decode('utf-8')

# Fields: List of rented items.
rented_items = ('The following equipment is rented and excluded in the Purchase Price. The Buyer agrees to assume the rental contract(s), if assumable:\n{}\nThe Buyer agrees to co-operate and execute such documentation, records and reports as may be required to facilitate such assumption.').decode('utf-8')

# Fields: The date the mortgage is due.
mortgage_date = ('Unless the Buyer gives notice in writing delivered to the Seller personally or in accordance with any other provisions for the delivery of notice in this Agreement or any Additional Terms thereto, by mutual agreement in writing the Buyer must arrange the aforementioned Charge/Mortgage not later than {}, that the Buyer has arranged, at the Buyer’s own expense, Charge/ Mortgage satisfactory to pay the balance of the purchase price, this offer shall be terminated and all monies paid refunded in full without interest or deduction to the Buyer. This condition is included for the benefit of the Buyer and may be waived at the Buyer’s sole option by notice in writing to the Seller as aforesaid within the time period stated herein.').decode('utf-8')

survey_date = ('The Seller agrees to provide, at the Seller’s own expense, not later than {}, an existing survey or new survey by a professional Land Surveyor, of said property showing the current location of all structures, buildings fences, improvements, easements, rights of way, and encroachments affecting said property. The Seller also agrees to supply all building plans, mechanical drawings, any other plans, and all warranties and services manuals, if available, applicable to any equipment or chattels included in the purchase price. The Seller will further deliver, on completion, a declaration confirming that there have been no additions to the structures, buildings, fences, and improvements on the property since the date of this survey.').decode('utf-8')

completion_date = ('This Agreement shall be completed by no later than the {} day of the {} month of the year {}. Upon completion, the Buyer will have vacant possession of the property unless otherwise provided for in this Agreement. The Seller warrants and represents that  the Seller has obtained a release from any prior Agreement of Purchase and Sale.').decode('utf-8')

chattels_and_fixs = ('The Seller represents and warrants that the chattels and fixtures as included in this Agreement will be in good working order and free from liens and encumbrances on completion. The parties in this Agreement of Purchase and Sale agree that this representation and warranty shall survive and not merge on completion of this transaction, but apply only to those circumstances existing at the date of completion stated herein.').decode('utf-8')

buyer_mrtg_arrange = ('This Offer is conditional upon the Buyer arranging, at the Buyer’s own expense, Charge/ Mortgage satisfactory to pay the balance of the purchase price. This condition is included for the benefit of the Buyer and may be waived at the Buyer’s sole option by notice in writing to the Seller as aforesaid within the time period stated herein.').decode('utf-8')

# Fields: None.
equipment = ('The Seller warrants and represents that all the mechanical, electrical, heating, ventilation, air conditioning systems, air compressors, elevators, conveyor systems, sprinkler systems, boilers, and all the other equipment on the real property shall be in good working order on completion. The Buyer and Seller agree that this warranty shall survive and not merge on the date of completion, but apply only to the state of the property at the date of completion stated herein.').decode('utf-8')

# Fields: None.
environmental = ('The seller represents and warrants that all environmental laws and regulations have been complied with, no hazardous conditions or substances exist on the land, no limitations or restrictions affecting the continued use of the property exist, other than those specifically provided for herein, with respect to environmental matters said environmental matters are not subject to any pending litigation, and no charges or prosecutions respecting environmental matter exist, there has been no prior use as a waste disposal site, no portion of the property has been designated as hazard land, floodplain, or an environmentally protected zone and all applicable licenses are in force. The Seller agrees to provide to the Buyer upon request, access to all documents, records and reports relating to environmental matters in possession of the Seller. The Seller further authorizes the appropriate Ministry, to release to the Buyer or the Buyer’s Solicitor, any and all information that may be on record in the Ministry office with respect to the said property. The parties in this Agreement agree that this representation and warranty shall survive and not merge on the date of completion of this transaction, but apply only to those circumstances existing at the date of completion. This condition is included for the benefit of the Buyer and may be waived at the Buyer’s sole option by notice in writing to the Seller as aforesaid within the time period stated herein.').decode('utf-8')

# Fields: None
maintenance = ('The Seller agrees to leave the premises, including the floors, in a clean and broom swept condition. The Seller agrees to clean, repair or replace any damaged floor covering in the building and permit the Buyer the right to inspect the premises to ensure that said cleaning, repairing or replacing has been completed. The Seller agrees to remove all equipment, storage containers and any other materials, including refuse and debris, from the property and to leave the parking area in a clean and vacant condition.').decode('utf-8')

uffi = ('Seller represents and warrants to Buyer that during the time Seller has owned the property, the Seller has not caused any building on the property to be insulated with insulation containing urea formaldehyde, vermiculite and/or any other hazardous substance which materially affects the use of the property, and that to the best of Seller’s knowledge no building on the property contains or has ever contained insulation that contains urea formaldehyde, vermiculite and/or other hazardous substance, which materially affects the use of the property. This warranty shall survive and not merge on the date of completion, and if the building is part of a multiple unit building, this warranty shall only apply to that part of the building which is the subject of this transaction.').decode('utf-8')

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
}

