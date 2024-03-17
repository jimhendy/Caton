import caton


def test_generate_random_terrains_with_4_players():
    n_players = 4
    terrain = caton.generate_random_terrains(n_players=n_players)
    expected = [3, 4, 5, 4, 3]
    assert len(terrain) == len(expected)
    for i in range(len(terrain)):
        assert len(terrain[i]) == expected[i]
        assert all(isinstance(hex, caton.Terrain) for hex in terrain[i])


def test_generate_random_number_tokens_with_4_players():
    n_players = 4
    number_tokens = caton.generate_random_number_tokens(n_players=n_players)
    expected = [3, 4, 5, 4, 3]
    assert len(number_tokens) == len(expected)
    for i in range(len(number_tokens)):
        assert len(number_tokens[i]) == expected[i]
        assert all(isinstance(token, int | None) for token in number_tokens[i])


def test_generate_random_terrains_with_6_players():
    n_players = 6
    terrain = caton.generate_random_terrains(n_players=n_players)
    expected = [3, 4, 5, 6, 5, 4, 3]
    assert len(terrain) == len(expected)
    for i in range(len(terrain)):
        assert len(terrain[i]) == expected[i]
        assert all(isinstance(hex, caton.Terrain) for hex in terrain[i])


def test_generate_random_number_tokens_with_6_players():
    n_players = 6
    number_tokens = caton.generate_random_number_tokens(n_players=n_players)
    expected = [3, 4, 5, 6, 5, 4, 3]
    assert len(number_tokens) == len(expected)
    for i in range(len(number_tokens)):
        assert len(number_tokens[i]) == expected[i]
        assert all(isinstance(token, int | None) for token in number_tokens[i])
