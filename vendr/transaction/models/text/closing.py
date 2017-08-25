# -*- coding: utf-8 -*-
# 
# Closing Document text.
# Note, for each document we have a set of different types -- one for each
# different property type (e.g. Condo, House, etc.).
#
# ==========================================================================

DOCUMENTS_TEXT = {

        # Buyer name. Seller name.
        'header': 'Buyer, {}\nSeller, {}'.decode('utf-8'),

        # Type of document. Date of signing.
        'footer':'CONFIRMATION OF ACCEPTANCE: Both parties confirm that they have accepted this {} on {}.\nPrint Name(s):'.decode('utf-8'),

        # Test for the Amendment document.
        # Date the contract was signed. List of amended clauses. Irrevocability date.
        'amendment': 'In accordance with the terms and conditions of the Agreement of Purchase and Sale dated, {}, regarding the said property above, I/We hereby agree to the following Amendments to the condition(s) which read(s) as follows: {}\nIRREVOCABILITY: This Offer to Amend the Agreement shall be irrevocable by [BUYER/SELLER] until {}, after which time, if not accepted, this Offer to Amend the Agreement shall be null and void.\nAll other terms and conditions in the aforementioned Agreement of Purchase and Sale to remain unchanged.\nFor the purposes of this Amendment, “Buyer” includes purchaser and “Seller” includes vendor. This amendment shall constitute the entire Agreement of Purchase and Sale between Buyer and Seller.\nTime shall in all respects be of the essence hereof provided that the time for doing or completing of any matter provided for herein may be extended or abridged by an agreement in writing signed by Seller and Buyer or by their respective solicitors who are hereby expressly appointed in this regard.'.decode('utf-8'),

        # Text for the Waiver document.
        # Date the contract was signed. List of waived clauses. Date this doc
        # was signed.
        'waiver':  'In accordance with the terms and conditions of the Agreement of Purchase and Sale dated {} regarding the said property above, I/We hereby waive the condition(s) which read(s) as follows:\n{}\nAll other terms and conditions in the aforementioned Agreement of Purchase and Sale to remain unchanged.\nFor the purposes of this Waiver, “Buyer” means purchaser and “Seller” means vendor. This waiver shall constitute the entire Agreement of Purchase and Sale between Buyer and Seller.'.decode('utf-8'),
        # Text for the Notice of Fulfillment document.
        # Date the contract was signed. List of contract requirements.
        'notice_of_fulfillment': 'In accordance with the terms and conditions of the Agreement of Purchase and Sale dated {}, regarding the said property above, I/We hereby confirm that I/We have fulfilled the condition(s) which read(s) as follows:\n{}\nAll other terms and conditions in the aforementioned Agreement of Purchase and Sale to remain unchanged.\nFor the purposes of this Notice of Fulfillment of Condition, “Buyer” means purchaser and “Seller” means vendor.'.decode('utf-8'),

        # Text for the Mutual Release document.
        # Date the contract was signed. Irrevocability date.
        'mutual_release':'In accordance with the terms and conditions of the Agreement of Purchase and Sale dated {}, regarding the said property above, I/We hereby agree to the following Mutual Release.\nWe, the Buyers and the Sellers in the above noted transaction hereby acknowledge that the above described transaction is terminated and release each other from all liabilities, covenants, obligations, claims and sums of money arising out of the above Agreement of Purchase and Sale, together with any rights and causes of action that each party may have had against the other and monies paid returned in full without interest or deduction to the Buyer.\nIRREVOCABILITY: This Mutual Release shall be irrevocable by [BUYER/SELLER] until {}, after which time, if not accepted, this Mutual Release shall become null and void.\nAll other terms and conditions in the aforementioned Agreement of Purchase and Sale to remain unchanged.\nFor the purposes of this Mutual Release, “Buyer” includes purchaser and “Seller” includes vendor. This release shall be binding upon the heirs, executors, administrators and assigns of all the parties executing same.\nTime shall in all respects be of the essence hereof provided that the time for doing or completing of any matter provided for herein may be extended or abridged by an agreement in writing signed by Seller and Buyer or by their respective solicitors who are hereby expressly appointed in this regard.'.decode('utf-8'),

        # Property address, square footage.
        'house_descriptor':'Real Property:\nAddress {} with a square footage more or less of {}.'.decode('utf-8'),

        # Property address, unit number.
        'condo_descriptor':'''A unit in the condominium property located at {}, Unit No. {}, together with Seller's proportionate undivided tenancy-in-common interest in the common elements appurtenant to the Unit as described in the Declaration and Description including the exclusive right to use such other parts of the common elements appurtenant to the Unit as may be specified in the Declaration and Description: the Unit, the proportionate interest in the common elements appurtenant thereto, and the exclusive use portions of the common elements, being herein called the "Property".'''.decode('utf-8'),

        # TODO: For legal reasons, Shares might need to be an actual field here.
        # The unit #. The address. The coop corporation.
        'coop_descriptor': 'Real Property and Shares:\nThe exclusive right to occupy and use Unit No. {} (the "Unit") in the Co-operative Apartment Building located at: {} (the “Property”) and shares (the "shares") in the Capital of {} (the "Corporation").'.decode('utf-8'),

        # Manufacturer, Serial #, Year, Length, Width, Address, mobile
        # home park.
        'manufactured_descriptor': 'Property:\nThe Manufactured property (the "Dwelling") more fully described as:\nManufacturer {}, Model (if applicable) {}, Serial Number {}, Year {}, Length {}, Width {}, \nLocated At: (address, lot/site number, etc.) {} the “Land”).\nName of Mobile Home Park (if applicable) {}.'.decode('utf-8'),

        # Address, square footage.
        'vacantland_descriptor': 'Real Property:\nAddress {} with a square footage more or less of {}.'.decode('utf-8')
}

