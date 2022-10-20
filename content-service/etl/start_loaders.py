import time

import loaders
import es
import log
from settings import settings
from state import State, JsonFileStorage


if __name__ == '__main__':
    entities = [
        'film_work',
        'genre',
        'person',
        'genres',
        'persons'
    ]
    storage = JsonFileStorage('all-state.json')
    state = State(storage)

    es.ensure_movies_index_exists()
    es.ensure_genres_index_exists()
    es.ensure_persons_index_exists()

    log.logger.info(entities)
    while True:
        for entity in entities:
            try:
                log.logger.info(f'By entity: "{entity}". Start loading.')
                loader = loaders.create_loader_for_entity(entity, state, settings, log.logger)
                loader.load()
            except Exception:
                log.logger.exception(f'Unexpected exception while loading films by entity "{entity}".')
            finally:
                log.logger.info(f'By entity: "{entity}". Finish.')

        time.sleep(20)
