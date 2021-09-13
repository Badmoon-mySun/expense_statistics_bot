import logging

from aiogram.utils import executor

from bot import bot, WEBHOOK_URL, dp, WEBHOOK_PATH, WEBAPP_HOST, PORT


# Run after startup
async def on_startup(_) -> None:
    logging.info('Starting connection.')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    logging.info(f'Bot was setting up with webhook url: {WEBHOOK_URL}')


# Run before shutdown
async def on_shutdown(_) -> None:
    logging.info("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info("Bot down")


if __name__ == "__main__":
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=PORT,
    )
