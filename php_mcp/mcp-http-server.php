<?php

declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';

use PhpMcp\Server\Server;
use PhpMcp\Server\Transports\StreamableHttpServerTransport;
use Psr\Log\AbstractLogger;
use Psr\Log\LoggerInterface;
use PhpMcp\Server\Defaults\BasicContainer;
use PhpMcp\Schema\ServerCapabilities;


class StderrLogger extends AbstractLogger
{
    public function log($level, \Stringable|string $message, array $context = []): void
    {
        fwrite(STDERR, sprintf("[%s][%s] %s %s\n", date('Y-m-d H:i:s'), strtoupper($level), $message, empty($context) ? '' : json_encode($context)));
    }
}

try
{
    $logger = new StderrLogger();
    $logger->info('Starting MCP HTTP Server...');

    $container = new BasicContainer();
    $container->set(LoggerInterface::class, $logger);

    $server = Server::make()
                    ->withServerInfo('HTTP User Profiles', '1.0.0')
                    ->withCapabilities(ServerCapabilities::make(completions: true, logging: true))
                    ->withLogger($logger)
                    ->withContainer($container)
                    ->build();

    $server->discover(__DIR__, ['src']);

    // $transport = new StreamableHttpServerTransport(
    //     host: '127.0.0.1',      // MCP protocol prohibits 0.0.0.0
    //     port: 8080,
    //     mcpPath: '/mcp',
    //     enableJsonResponse: false,  // Use SSE streaming (default)
    //     stateless: false            // Enable stateless mode for session-less clients
    // );

    $transport = new StreamableHttpServerTransport('127.0.0.1', 8080, 'mcp');

    $server->listen($transport);

    $logger->info('Server listener stopped gracefully.');
    exit(0);

} catch (\Throwable $e) {
    fwrite(STDERR, "[CRITICAL ERROR] " . $e->getMessage() . "\n");
    exit(1);
}