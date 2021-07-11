import os
from nose import tools as ntools
from draftfast.optimize import run
from draftfast import rules
from draftfast.csv_parse import salary_download
from draftfast.orm import Player

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
salary_file = '{}/data/dk-mlb-salaries.csv'.format(CURRENT_DIR)


def test_mlb_dk():
    player_pool = salary_download.generate_players_from_csvs(
        salary_file_location=salary_file,
        game=rules.DRAFT_KINGS,
        ruleset=rules.DK_MLB_RULE_SET,
    )
    roster = run(
        rule_set=rules.DK_MLB_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )

    # Test general position limits
    ntools.assert_not_equal(roster, None)
    ntools.assert_true('RP' in [x.pos for x in roster.players])


def test_five_batters_max():
    player_pool = [
        Player(pos='P', name='A', cost=5000, team='C'),
        Player(pos='P', name='B', cost=5000, team='B'),

        Player(pos='1B', name='C', cost=5000, team='C'),
        Player(pos='OF', name='H', cost=5000, team='C'),
        Player(pos='OF', name='I', cost=5000, team='C'),
        Player(pos='C', name='F', cost=5000, team='C'),
        Player(pos='2B', name='D', cost=5000, team='C'),
        Player(pos='2B', name='E', cost=5000, team='C'),
        Player(pos='3B', name='E', cost=5000, team='C'),

        Player(pos='SS', name='G', cost=5000, team='Q'),
        Player(pos='OF', name='J', cost=5000, team='G'),
    ]

    roster = run(
        rule_set=rules.DK_MLB_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    assert roster is None

    player_pool.append(Player(pos='3B', name='EA', cost=5000, team='A'))
    roster = run(
        rule_set=rules.DK_MLB_RULE_SET,
        player_pool=player_pool,
        verbose=True,
    )
    c_in_roster = [
        x for x in roster.players
        if x.team == 'C'
        and x.pos != 'P'
    ]

    assert len(c_in_roster) < 6
