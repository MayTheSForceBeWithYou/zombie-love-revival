## Smoke tests — no dialogue, transitions, or audio (avoids GUI hangs in test mode).

testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 5.0

    teardown:
        exit

## Smoke test for CI. Keep this deterministic and fast.

testcase smoke_start:
    $ init_relationships()
    $ init_inventory()
    $ init_missions()
    assert eval relationships["crow"]["affection"] == 1
    assert eval inventory["bandage"] == 3
    assert eval missions["find_the_pharmacy"]["status"] == "inactive"
