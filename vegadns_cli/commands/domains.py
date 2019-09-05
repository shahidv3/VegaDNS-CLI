from builtins import str
import click
import json
import logging

from vegadns_client.exceptions import ClientException
from vegadns_cli.common import domains


logger = logging.getLogger(__name__)


@domains.command()
@click.option(
    "--search",
    default=False,
    help="Optionally search domain names"
)
@click.option(
    "--include-permissions",
    is_flag=True,
    default=False,
    help="Includes your permissions on each domain"
)
@click.pass_context
def list(ctx, include_permissions, search):
    """List domains"""
    try:
        collection = ctx.obj['client'].domains(search, include_permissions)
        domains = []
        for domain in collection:
            domains.append(domain.values)
        click.echo(json.dumps(domains, indent=4))
    except ClientException as e:
        click.echo("Error: " + str(e.code))
        click.echo("Response: " + e.message)
        ctx.exit(1)


@domains.command()
@click.option(
    "--domain",
    type=str,
    help="domain name"
)
@click.option(
    "--domain-id",
    type=int,
    help="ID of the domain, takes precedence"
)
@click.option(
    "--include-permissions",
    is_flag=True,
    default=False,
    help="Includes your permissions on each domain"
)
@click.pass_context
def get(ctx, include_permissions, domain_id=None, domain=None):
    """Get a single domain"""
    try:
        if domain_id is not None:
            d = ctx.obj['client'].domain(domain_id)
            click.echo(json.dumps(d.values, indent=4))
            ctx.exit(0)

        if domain is None:
            domain = click.prompt('Please enter the domain name')

        collection = ctx.obj['client'].domains(domain, include_permissions)
        domains = []
        for dom in collection:
            domains.append(dom.values)

        for d in domains:
            if d["domain"] == domain.lower():
                click.echo(json.dumps(d, indent=4))
                ctx.exit(0)

        # not found
        click.echo("Error: domain not found: " + domain)
        ctx.exit(1)
    except ClientException as e:
        click.echo("Error: " + str(e.code))
        click.echo("Response: " + e.message)
        ctx.exit(1)


@domains.command()
@click.option(
    "--status",
    type=str,
    help="Domain status, can be 'active' or 'inactive'"
)
@click.option(
    "--owner-id",
    type=int,
    help="Account id of domain owner"
)
@click.option(
    "--domain-id",
    type=int,
    prompt=True,
    help="ID of the domain, required"
)
@click.pass_context
def edit(ctx, domain_id, owner_id, status):
    """Edit a domain"""
    try:
        d = ctx.obj['client'].domain(domain_id)
        d.edit(owner_id, status)
        click.echo(json.dumps(d.values, indent=4))
    except ClientException as e:
        click.echo("Error: " + str(e.code))
        click.echo("Response: " + e.message)
        ctx.exit(1)


@domains.command()
@click.option(
    "--move-colliding-records",
    is_flag=True,
    default=False,
    help=("Move any records whose label collides with this domain into "
          "the new domain")
)
@click.option(
    "--skip-default-records",
    is_flag=True,
    default=False,
    help="Skip creation of default records"
)
@click.option(
    "--skip-soa",
    is_flag=True,
    default=False,
    help="Skip just the default SOA record creation"
)
@click.option(
    "--domain",
    type=str,
    prompt=True,
    help="Domain name, required and must be unique"
)
@click.pass_context
def create(ctx, domain, skip_soa=False, skip_default_records=False,
           move_colliding_records=False):
    """Create a new domain"""
    try:
        d = ctx.obj['client'].domains.create(
            domain, skip_soa, skip_default_records, move_colliding_records
        )
        click.echo(json.dumps(d.values, indent=4))
    except ClientException as e:
        click.echo("Error: " + str(e.code))
        click.echo("Response: " + e.message)
        ctx.exit(1)


@domains.command()
@click.option(
    "--domain-id",
    type=str,
    prompt=True,
    help="Domain id, required"
)
@click.pass_context
def create_default_soa(ctx, domain_id):
    """Creates an SOA record using the default SOA record"""
    try:
        d = ctx.obj['client'].domain.create_default_soa(domain_id)
        click.echo(json.dumps(d.values, indent=4))
    except ClientException as e:
        click.echo("Error: " + str(e.code))
        click.echo("Response: " + e.message)
        ctx.exit(1)


@domains.command()
@click.option(
    "--domain-id",
    type=int,
    prompt=True,
    help="ID of the domain, required"
)
@click.pass_context
def delete(ctx, domain_id):
    """Delete a domain"""
    try:
        d = ctx.obj['client'].domain(domain_id)
        d.delete()
    except ClientException as e:
        click.echo("Error: " + str(e.code))
        click.echo("Response: " + e.message)
        ctx.exit(1)
