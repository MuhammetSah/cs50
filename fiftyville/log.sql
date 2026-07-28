-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Calling all crimes which took place at 2025 July 28th in Humphrey Street
SELECT year,description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Crime took scene at 10:15 at a Bakery. Three witnesses gave interviews which were present at this time. So calling all transcript which took place at this date
SELECT transcript FROM interviews WHERE year = 2025 AND month = 7 AND day = 28;

--(Information out of transcripts) Thief withdraw money at the Leggett Street -- Thief used a car = Check camera footage --Called someone for less than a minute-wants to fly tomorrow (early)
-- 1. Check security Logs for the license plate
SELECT license_plate FROM bakery_security_logs WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 and 25 AND activity = 'exit';
-- Possible license_plates = 5P2BI95 // 94KL13X // 6P58WS2 // 4328GD8 // G412CB7 // L93JTIZ // 322W7JE // 0NTHK55

-- 2. Check atm_transactions for withdrawals at this time
SELECT account_number FROM atm_transactions WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' and transaction_type = 'withdraw';
-- Possible account_numbers 28500762 // 28296815 // 76054385 // 49610011 // 16153065 // 25506511 // 81061156 // 26013199

-- 3. Check the phone_calls
SELECT caller, receiver FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 61;
-- Possible caller (130) 555-0289 | (499) 555-9472 | (367) 555-5533 | (499) 555-9472 | (286) 555-6063 | (770) 555-1861 | (031) 555-6622 | (826) 555-1652 | (338) 555-6650

-- Checking where the thief flew away because he wanted to take the earliest flight on 29th July 2025
SELECT destination_airport_id FROM flights WHERE year = 2025 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;
-- ID of destination is 4. Checking which id corresponds to that airport
SELECT city FROM airports WHERE id = 4;
-- Thief flew to New York City

-- Trying to find the Thief with given license_plate, account_number and phone number
SELECT name FROM people WHERE id IN
(
    SELECT person_id FROM bank_accounts WHERE account_number IN
    (
        SELECT account_number FROM atm_transactions WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' and transaction_type = 'withdraw'
    )
)
AND phone_number IN
(
    SELECT caller FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 61
)
AND license_plate IN
(
    SELECT license_plate FROM bakery_security_logs WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 and 25 AND activity = 'exit'
)
AND passport_number IN
(
    SELECT passport_number FROM passengers WHERE flight_id =
    (
        SELECT id FROM flights WHERE year = 2025 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1
    )
);
-- Thief is Bruce

-- Trying to find the accomplice, since we know its Bruce, we just have to check on the receiver from the call Bruce took
SELECT name FROM people WHERE phone_number IN
(
    SELECT receiver FROM phone_calls WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 61 and caller =
    (
        SELECT phone_number FROM people WHERE name = 'Bruce'
    )
);
-- Accomplice is Robin

-- Case closed
