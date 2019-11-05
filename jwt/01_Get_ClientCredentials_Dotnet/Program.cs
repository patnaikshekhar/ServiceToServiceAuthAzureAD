using System;
using Microsoft.Identity.Client;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration.Json;
using Microsoft.Extensions.Configuration;

namespace _01_Get_ClientCredentials_Dotnet
{
    class Program
    {
        

        static async Task Main(string[] args)
        {
            var config = new ConfigurationBuilder()
                .AddJsonFile("config.json")
                .Build();
            
            var clientID = config["client_id"];
            var clientSecret = config["client_secret"];
            var tenantID = config["tenant_id"];

            var client = 
                ConfidentialClientApplicationBuilder
                    .Create(clientID)
                    .WithClientSecret(clientSecret)
                    .WithTenantId(tenantID)
                    .Build();
            
            var token = await client.AcquireTokenForClient(new[] { "api://sampleserviceA/.default" }).ExecuteAsync();
            
            Console.WriteLine($"Token is {token.AccessToken}");
        }
    }
}
