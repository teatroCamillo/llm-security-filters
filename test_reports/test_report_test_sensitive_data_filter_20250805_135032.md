# 🧪 Test Report for `test_sensitive_data_filter` (2025-08-05 13:50:32.879719)

Total tests: 442

- `tests/unit/test_sensitive_data_filter.py::test_should_initialize_with_default_weight` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_initialize_with_valid_weight` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_raise_error_for_weight_out_of_bounds[-0.01]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_raise_error_for_weight_out_of_bounds[-10]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_raise_error_for_weight_out_of_bounds[10.01]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_raise_error_for_weight_out_of_bounds[100]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_weight_at_boundary_values[0.0]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_weight_at_boundary_values[10.0]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[John Doe's email is john.doe@example.com]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call me at 555-123-4567 after 5 PM]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[My credit card number is 4111 1111 1111 1111]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Social Security Number: 123-45-6789]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Jane's address is 123 Maple Street]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: 987654321]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Her phone number is (212) 555-7890]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Contact support@company.org for access]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Patient ID: P-00199233]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He transferred $10]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 62th in the race UUID: ab5d3d33-24a9-4e1c-8278-a83b52c56505 Key: e49b5c7a9e738d485bc77b54d9906a928859295bcd805a4600efcb51f1588e9e]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Be there at 07:13:41 Email: cindy80@yahoo.com They ordered 350 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in Florida beyond claim]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: EFAD41649291265884 Visit https://burke.com/ international]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[License number: D-69835476 week peace example]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Be there at 16:15:09 SSN: 731-58-7227]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: d4f0bc5a29de06b510f9aa428f1eedba926012b591fef7a518e776a7c9bd1824 They ordered 490 units PAD record: P-357571]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 2th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Credit card: 4220653765209226560 She lives in Massachusetts The event is on 1989-09-10]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 0d0d9c8c-e7b8-4352-aae0-f8533496d2dd Bank account: VCWC03160102142822 commercial]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit https://www.valencia.info/ The package was sent to PSC 3837]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit http://www.martin.com/ edge worker throughout skill]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1974-09-14 IPv6: b105:22ee:c637:8a98:3f71:5981:ca9b:132b]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 8th in the race Bank account: CNTW51921167394724]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 3a63e044-3188-4cb0-8815-a8b47c7347c1 wide station issue receive]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: ca1c:5e43:25:d896:feec:f327:3e4c:da62 my either rate hear]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit http://www.sims.net/ live nature else purpose]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 496-76-8296 IPv6: fde4:1e28:d3a9:b295:c425:72a4:c9b6:8fd3 deal pattern]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-346717 License number: D-90066225]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IP address: 145.88.163.56 Call at 0457783741]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 345.838.7898 He finished 49th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1999-03-14 just]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in Iowa He finished 80th in the race License number: D-3559364]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit https://reid-washington.com/ Credit card: 3515165502445664 American]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: TVRA13129627388625 PAD record: P-835869]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 7d:73:bc:65:9a:6e UUID: 670a601f-9e6f-492c-8ad8-ec7f1a8ca91a License number: D-67764944]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 82th in the race Call at 439.798.1063]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Credit card: 379335800867189 The event is on 2025-04-06]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: 31be:6189:99bc:f61f:bc58:70d4:2cfb:b95c wall rate before price]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The score was 99.29 difficult for]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 920.192.7519x235 MAC: bd:28:3f:af:c3:64 He finished 35th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 272-23-8285 They ordered 281 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[They ordered 26 units SSN: 180-31-9381 IP address: 44.92.3.115]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The package was sent to 747 Linda Isle]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The package was sent to 3196 Noble Groves]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[License number: D-56249009 SSN: 524-85-0382 The package was sent to PSC 6079]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-309258 The score was 19.47]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Be there at 18:28:46 maintain right]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 2016-10-05 size]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IP address: 197.28.95.218 gun despite general]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 85:57:38:da:6a:70 IP address: 137.140.147.187 fast]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: gjackson@gmail.com Timestamp: 2005-10-31 23:28:34 then]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 523-236-5060x470 Be there at 16:06:58 Bank account: UVUL18158179576582]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 75th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IP address: 29.224.21.170 License number: D-95233699 She lives in Maine]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IP address: 29.37.214.136 letter stop customer]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 879-59-1233 IPv6: c188:69d:2ca7:dbc1:f760:4d55:1e49:e8a8 word station]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The package was sent to 37793 Molly Corners Apt. 779]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 899-60-0292 Call at +1-489-456-9233 Email: hdiaz@gmail.com]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: HJSC48953492276737 bank conference herself]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: SOVN71095651750805 PAD record: P-121901]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: 6342d0648a74645722ea17901df180d13ab12ce64c01f16e846e39a01eae8419 Bank account: JDHE25237293266666 Credit card: 4734402037733]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The package was sent to 06347 Joyce Shore]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-811142 Email: zmerritt@jarvis.net ready]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: stephen22@gmail.com PAD record: P-183362 hundred]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: pburns@gmail.com company wide fast onto]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: 2740e59ffb8c5eff0e0f8f3f4f5e6522fda77d9882c878346a751b9b60129cfd teacher ok west fire]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 53th in the race They ordered 113 units Credit card: 3528022939448305]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 7fb9726c-6439-459a-8d99-2f1e1d1c28f8 would meet early toward]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Be there at 12:36:52 MAC: 6d:f2:86:5e:9f:da]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 1a:b4:05:ab:9f:10 newspaper trial seem so]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The score was 85.24 Bank account: HXNH04065090567012]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The score was 79.37 License number: D-54790156 The event is on 2017-11-24]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: 9f6eec7d586f63c4644e1512293d038bd57d66c8a3bdfcfc0a9c3c3a71d12515 idea sound relate represent]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit https://www.clarke.com/ PAD record: P-636670 wish]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 47th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The score was 0.21 decision kitchen]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Timestamp: 2009-03-05 05:23:50 PAD record: P-636422 The package was sent to 699 Carter Summit Suite 738]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The package was sent to 3785 Ricky Brook]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1971-01-19 The package was sent to 016 Potter Port Apt. 689]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 94:31:37:9b:1d:ef Credit card: 30027839340855 without]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: c7d6:7fa9:b1ab:f21f:2a55:4b10:72cb:6b5f Be there at 02:17:24 Bank account: XLGI56575687346306]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: a2a1de68-1015-4e73-be7b-140c7bf35468 License number: D-30275496 same]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[License number: D-99057986 Visit http://www.estes-johnson.com/ The package was sent to 330 Erickson Key Apt. 512]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 5a:35:cf:39:d8:fa Credit card: 2226286565524658 lot]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1996-12-01 also]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: f9:33:c7:a0:f7:23 The event is on 1986-12-13]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IP address: 130.139.175.25 Email: bhayes@yahoo.com claim]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: ALBZ79624716351689 around support line]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[They ordered 166 units reduce seat]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: dd1b3c312cf7d816130354452e9629ce39355b0c534129dd26a08cd9a4502ede Email: nmartinez@yahoo.com need field]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: e27c:2fc0:6dba:dc83:daa8:7488:8b0e:2098 PAD record: P-693321 spend]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: timothygonzalez@woodward.com UUID: e8c783a7-f3aa-4fe5-90a5-e84969fd0e99 Be there at 11:26:04]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 9509a0cf-15fb-4fc5-bafa-975e37e6b386 IP address: 65.92.192.139 Credit card: 2720373358827430]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Be there at 02:58:14 from woman]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: e91fadf24f78c081972a2015146e9b7ad4636bb5a208f5733b54ee4407682078 experience fire run whole]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit https://leon.net/ SSN: 671-64-3500 Credit card: 6586154172342085]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-103307 He finished 63th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1994-04-01 resource]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: 2267:3e0f:420a:8275:fe8f:8faa:3b51:a46b The score was 9.43]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 7884b4eb-979a-4093-bda4-be19a0dc1890 debate as friend threat]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1973-04-07 License number: D-27911266 Call at 495.714.1632]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 4c:47:70:dd:d8:30 SSN: 301-35-6948 They ordered 273 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 89th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IP address: 9.40.25.221 License number: D-95914429 The event is on 2019-10-24]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Be there at 20:04:05 we event]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 640-71-9230 IPv6: 1ea:3395:bd44:529a:f90:67d5:ca80:1a22 moment become]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-223633 The score was 30.2]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: HTQM29986354959198 those environment court]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-941568 MAC: 57:58:c3:fb:1d:e4 property]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: KRBS56438534797804 Be there at 12:10:31 The package was sent to 47313 Brian Circles]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[License number: D-54977207 Email: ulane@gmail.com baby]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: RQRB67775655788959 UUID: bfa8ff6e-62fc-4ab5-8922-49cfe3c1f41e License number: D-2203355]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: 8d11:f1a0:4f14:f991:1fc6:51a:28a4:8e0a key admit thought character]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 2007-03-06 Call at 7734949348]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 264-22-3685 License number: D-56996298 She lives in Utah]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: 47fc:3797:17e5:393f:e7ee:e338:b324:be40 He finished 78th in the race The score was 52.63]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: FGHD42632065330661 They ordered 356 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 551-034-4165x665 expert finish it]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 17:9c:35:dd:20:9b Key: 34235a2c502e3919d3f00af5dabb87cb58aef4566b10631f2a5db94950ebffbd License number: D-73717131]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IP address: 173.207.106.72 investment similar continue]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 702.094.2798 Bank account: JKCF54832152133597]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: d0:05:82:8e:6f:5f PAD record: P-323830 first]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: kristin68@santos.biz The score was 37.43]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at +1-433-671-6666x36091 They ordered 405 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Credit card: 4124420681725548 Be there at 01:27:57 Email: jeremynavarro@gmail.com]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: a56:33e6:3e66:f0ed:8453:a221:d6a8:318 IP address: 133.120.153.107 manage]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: fe:15:c3:79:e7:9f ground former American few]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 638-769-6360 look follow five]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1980-04-15 Key: 276446ba01e3aa387c83b06f54fccc5ac65bdc6099157a2a828716eac9c6fd4d]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: bdaniels@yahoo.com IPv6: 46e5:6872:1c5e:3155:5bf5:2f6b:4616:193f letter check]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 834df7e6-5d96-487f-b564-d4f3ca8a1c9c PAD record: P-907151 common]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 778-10-5814 Call at 275.430.4275x337 MAC: c6:b7:fd:74:f6:c9]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in Delaware SSN: 499-88-8472 PAD record: P-930292]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in New Jersey UUID: 5d5209fd-abca-46e1-ae37-7a448839b14d]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in Virginia Credit card: 347905560013734 The event is on 2010-10-07]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: 9ba0:a14f:4d6c:ffc0:e53a:1adc:35cb:39f9 License number: D-34349426 The package was sent to 51743 Graham Island Suite 268]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 8d0b97a4-a57c-4b25-a6a4-1b9960661625 Visit https://www.riley.net/ IPv6: 9a41:939c:1288:2b15:b652:1738:c959:fa43]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: d4f9cd97-433e-4804-b9a1-65bd2f932a04 The event is on 1972-03-19 Key: 45569da57f4b7bf472d7a864ef4781451cae6383fee9fb0ae40c59aa1ce475b7]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The score was 57.75 Key: 39d02b42938b2b75d027ebeb25c9d1fd0b71b6e0453e217a2e85cedc7e4637b4 She lives in Michigan]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 24th in the race UUID: f0f2eff2-6886-45c0-b534-d91edf600e6a]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Credit card: 5440456938654945 democratic picture energy]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: f14beadb-a054-4c80-8db6-281e84e27911 She lives in North Dakota]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 412-31-8500 land lead no office]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: LQZK88012381727156 Email: suzanne00@jenkins.com green]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: glogan@austin.com Visit http://fletcher-daniel.info/ live include]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: jeffreyrandolph@gmail.com They ordered 219 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[They ordered 384 units rather sort]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The score was 62.12 IPv6: b8f7:a9c8:2313:ccf9:1d86:834e:2bc1:5264 License number: D-47119194]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 413-677-2406 The event is on 1992-04-08]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[License number: D-42673234 He finished 71th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: simmonsmegan@gmail.com Be there at 17:22:53]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[UUID: 836a2fea-19c3-4520-93f8-374fc1c54c09 She lives in Oregon Key: cf929d06a4e69002b7b2d3fd991a129969aa5545c6c855f9efc2f17b4e7e3128]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 22th in the race The score was 53.22]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-185772 Bank account: MIAW72434205998854 Email: randall90@gross-jones.com]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Credit card: 4975677471939 IP address: 23.173.226.160 The event is on 1995-05-11]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[License number: D-33918208 prove occur computer]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in Georgia PAD record: P-356305 He finished 26th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: denise75@gmail.com They ordered 388 units Credit card: 30545056668757]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Timestamp: 2013-01-03 13:14:50 PAD record: P-300206 IP address: 75.226.151.97]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 2013-06-14 IPv6: c24a:ee0c:400:4be4:7b9b:b39d:eaf9:ef68]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Timestamp: 2003-04-15 11:14:34 The package was sent to 7301 Dawn Mills Apt. 218]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in Florida UUID: 7c23316c-3a8a-463d-86a2-8a68023819d6 MAC: c8:06:fd:33:c1:e1]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Call at 5297140910 home get story]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: c207:6de9:21b8:8128:5922:2d16:7369:be03 License number: D-72740947 Call at 001-362-217-1322]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: 60c411b2baec2ab58d4494dd7a1efcec94ed33e8737a24a920ab58a59284208d PAD record: P-925679 The score was 0.04]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 2011-01-04 interesting]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: khernandez@ortiz.net She lives in Wisconsin IP address: 22.230.230.247]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[License number: D-12491133 already while world]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: e0c9:ac2d:7c83:3e55:e4d5:a4da:22e2:1f07 UUID: 61ea6445-0ce5-4ca3-a5cf-5f947676a6f8 already author]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 2007-09-20 He finished 26th in the race Call at 001-018-442-5777x575]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 1987-11-07 Timestamp: 2022-03-13 12:26:05 UUID: acf6da8e-1813-4a55-86e9-db76449cc18f]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 94th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 9th in the race License number: D-86449022 Be there at 07:27:26]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Credit card: 4410449944224109 Mr his herself]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: ac:f7:62:ba:cb:18 Timestamp: 2000-12-23 09:30:44 the]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit https://gates-ross.com/ He finished 35th in the race]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[She lives in Florida catch all]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit http://www.krueger.info/ structure wear mention when]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The score was 43.47 Visit https://www.wood.biz/ Email: christopher44@hotmail.com]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Email: brandonmcfarland@alvarado-howell.com He finished 10th in the race Visit https://www.barnett-watson.com/]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Key: 3cc610240ec72ccfbf16c22bcd5d1d298a09f0e2bb1dd8feef426911542492c4 Credit card: 4818800771169766077 pretty]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-692356 Bank account: CYBX35807522116306 IP address: 103.28.62.141]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Be there at 19:25:11 She lives in Connecticut Credit card: 577296767384]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 582-25-2454 The event is on 2016-05-31]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 18th in the race License number: D-621008 Be there at 03:42:51]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 40:fc:2c:9c:91:6e face collection traditional national]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The package was sent to 58158 Dominique Trail Suite 328]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[The event is on 2024-10-10 Timestamp: 1998-03-09 12:19:31]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Visit http://www.hernandez-mack.com/ Timestamp: 2020-03-22 11:42:55 IPv6: ea22:71c3:a0c1:2b26:8e34:f2af:2cfc:6ac5]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 031-03-7766 plant two discuss assume]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 893-84-0405 UUID: 6d328f2c-c79d-4599-8f5a-666bee2a9d21 put officer]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Bank account: HYFT01762287470103 Be there at 05:03:07 IPv6: f958:ef66:64ee:e366:c49e:de40:a0a0:1c63]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[PAD record: P-617555 Credit card: 4872754037921748 Email: wayne08@gmail.com]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[IPv6: 47bc:b9e1:c7af:dc17:d549:650c:e656:ff59 challenge hand probably lose]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Timestamp: 1986-09-13 05:46:48 MAC: 85:35:fe:e0:74:d2 have]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Credit card: 3570914964142901 She lives in Ohio They ordered 394 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[MAC: 53:f8:55:4d:89:55 Key: 859169b38185780daa5497983ff20d2994390058d8a71f2847ac7846f970971e They ordered 244 units]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[SSN: 322-34-6197 require speak people sort]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[Timestamp: 1978-05-09 11:24:21 He finished 62th in the race Key: 97c10efe01d5c9c88704a12d361d8429b3a6aa2412290a0773109d5d2d603d5e]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_block_when_sensitive_data_detected[He finished 9th in the race MAC: a1:99:3b:9c:7b:09]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun is shining brightly this morning.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She enjoys reading books by the fireplace.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We went for a long walk along the river.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I had a delicious sandwich for lunch today.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The children played happily in the park.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He is learning to play the guitar on weekends.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They visited the museum on their holiday.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This movie has a really interesting plot.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She painted the room a lovely shade of blue.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We are planning a picnic for next Saturday.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher read during the weekend with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I love different cultures before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher build their homework before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He paint at home with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat explore movies when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer0]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book hate delicious food in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend always enjoy movies.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun always enjoy every morning.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He study interesting topics every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We eat after school during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer1]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer2]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I paint different cultures before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[You learn during the weekend.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes0]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They sleep books when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend prefer every morning in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She study the beach during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer3]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher run in the park with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes1]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book play books before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat walk in the park with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We visit the beach every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They play movies when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea eat new recipes before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer4]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They enjoy every morning with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book love with friends.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun love during the weekend before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The dog visit at home with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat write in the park when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They visit the beach every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer5]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher study the beach during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It run during the weekend with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I always hate with friends.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher build at home.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He enjoy interesting topics during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They prefer books when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She walk the beach during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She write their homework in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher write their homework in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea watch books before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They sleep different cultures before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I watch books in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It love different cultures when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat always write after school.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea always study during the weekend.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It run with friends before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The dog always like in the park.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat run during the weekend in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It explore the beach with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The dog enjoy after school during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun always walk different cultures.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat drink their homework in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun build delicious food in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We prefer interesting topics during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book walk the beach during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat sleep new recipes.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We watch music every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We enjoy after school before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend walk with friends in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He always read different cultures.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend run in the park when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend read during the weekend in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He write music before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They write at home in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun sleep books in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It study books in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun play every morning in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The kids always learn books.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book run delicious food when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat drink after school.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea learn movies during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun enjoy new recipes when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Do you like ice cream?]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book always paint delicious food.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer6]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea explore music during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea study music in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer7]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He drink delicious food during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher build the beach before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We walk during the weekend in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We walk new recipes in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer8]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher build books before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book prefer delicious food in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Is he going to the party?]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I always visit different cultures.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer9]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Did you call your mom?]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer10]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[You drink the beach in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend always paint in the park.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea always visit books.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He love new recipes before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We paint after school before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We read after school in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes2]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book paint every morning with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes3]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It like movies during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The kids paint in the park during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They play with friends with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea build during the weekend with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes4]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She read music when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer11]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun visit different cultures when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes5]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes6]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She sleep every morning before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[You study movies in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend explore books during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes7]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They always play at home.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer12]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We walk during the weekend.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book paint at home.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat always learn new recipes.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun play at home with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We study music before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book visit different cultures in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The dog run new recipes before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It write their homework during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They always play in the park.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea eat after school every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer13]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat always enjoy at home.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She enjoy books in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He paint during the weekend with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat learn delicious food before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes8]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer14]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes9]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat build at home before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat play after school when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea paint in the park every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer15]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes10]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher always drink different cultures.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat prefer books before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[You love during the weekend with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book study movies in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our teacher learn delicious food every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat build books in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend like delicious food.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I explore every morning when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We visit in the park before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer16]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer17]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It enjoy during the weekend before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He learn during the weekend with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea enjoy after school every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes11]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat like different cultures with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He run different cultures before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[We like their homework in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Are we ready to go?]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes12]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I drink books every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The sun always learn during the weekend.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book study different cultures in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She always watch interesting topics.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes13]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer18]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[That idea always watch with friends.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes14]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer19]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes15]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The dog always love music.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He like music during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She learn with friends before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Sometimes16]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It paint different cultures when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I paint delicious food in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[I visit new recipes with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book always learn at home.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[You always love different cultures.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer20]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This book sleep every morning.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They drink with friends with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He read during the weekend when it rains.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He drink in the park.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Have they seen that movie?]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Can she play the piano?]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[In summer21]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It walk in the park every day.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The dog run in the park during holidays.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[He play different cultures with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[My friend explore music with joy.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[It always paint different cultures.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[You learn the beach before bedtime.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The cat love delicious food in the evening.]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The weather today is sunny with mild winds]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[She enjoys painting landscapes on weekends]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Our team is meeting at 3 PM in the conference room]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[This software release includes several performance improvements]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[They hiked the Blue Ridge Mountains last summer]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Please review the project proposal by Friday]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[The coffee machine is located near the front desk]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Reading fiction helps improve creativity and empathy]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Welcome to our new employee orientation session]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_when_no_sensitive_data_detected[Lunch options include salad]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_on_empty_input` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_on_whitespace_only` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_handle_long_text` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_should_allow_if_labeler_fails` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score_with_empty_entity_list` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities0-1.0]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities1-0.2]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities2-0.6]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities3-0.4]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities4-0.17]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities5-0.0]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities6-0.63]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities7-0.7]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities8-1.0]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities9-0.47]` — ✅ PASSED

---

- `tests/unit/test_sensitive_data_filter.py::test_compute_risk_score[entities10-0.1]` — ✅ PASSED

---


---

## ✅ Summary

- Total: 442
- ✅ Passed: 442
- ❌ Failed: 0
- ⚠️ Skipped: 0
