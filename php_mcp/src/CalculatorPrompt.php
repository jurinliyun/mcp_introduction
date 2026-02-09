<?php

namespace App;

use PhpMcp\Server\Attributes\McpPrompt;
use Psr\Log\LoggerInterface;

#[McpPrompt(name: 'hr_add_number_prompt', description: 'Add two numbers together')]
class CalculatorPrompt
{
    public function __construct(
        private readonly LoggerInterface $logger
    ) {
    }

    public function __invoke(int $a, int $b): array
    {
        $this->logger->info('Prompt triggered: hr_add_number_prompt', ['a' => $a, 'b' => $b]);
        
        $text = "You are given two numbers: $a and $b.

Step 1: Call the MCP tool 'calculate_power' with base=$a and exponent=$b to calculate $a^$b.
Step 2: Call the MCP tool 'hr_add_numbers' with a=$a and b=$b to calculate $a + $b.
Step 3: Add the results from Step 1 and Step 2 together.
Step 4: Present the final result in words with emoji style.

Example format: 'The power result is X, the addition result is Y, and the combined total is Z. 😊'";

        return [['role' => 'user', 'content' => $text]];
    }
}